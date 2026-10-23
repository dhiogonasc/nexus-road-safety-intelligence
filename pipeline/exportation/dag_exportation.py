"""pipeline/exportation/dag_exportation.py"""

from functools import partial
from prefect import flow

from settings import bucket_settings, postgres_settings
from src.shared.utils.fn import named_partial
from src.pipeline.index import PIPELINE_CONFIG
from src.shared.pipeline.task import (
    task_create_schema,
    task_create_table,
    task_open_bucket_operation,
)
from src.shared.db.connection import create_connection
from src.shared.db.operation import (
    attach_connections,
    bootstrap_table,
    create_table,
    load_extensions,
)


@flow(
    name="Exportation",
    flow_run_name="flow_exportation: {domain}",
)
def flow_exportation(
    database: str,
    domain: str,
) -> None:
    """Orquestra a exportacao de um dominio para postgres"""

    domain_pipeline_config = PIPELINE_CONFIG.get_domain_config(domain=domain)
    assets = domain_pipeline_config.exportation

    load_extensions_fn = partial(
        load_extensions,
        extensions=[
            "postgres",
            "httpfs",
            "parquet",
        ],
    )
    catalog = postgres_settings.DB_NAME
    attach_connections_fn = partial(
        attach_connections,
        connections=[
            {
                "conn_string": postgres_settings.postgres_conn_string,
                "conn_alias": catalog,
                "conn_option": "(TYPE POSTGRES)",
            }
        ],
    )
    conn_fn = partial(
        create_connection,
        load_extensions_fn=load_extensions_fn,
        attach_connections_fn=attach_connections_fn,
        database=database,
    )
    schema_future = task_create_schema.submit(
        conn_fn=conn_fn,
        schema="analytics",
        catalog=catalog,
    )

    asset_futures = {}

    for asset in assets:
        wait_tasks = [schema_future]

        table = asset.table
        upsert_fn = asset.upsert_fn
        depends_on = asset.depends_on

        for dependency in depends_on:
            if dependency.table.name in asset_futures:
                wait_tasks.append(asset_futures[dependency.table.name])

        create_table_future = task_create_table.submit(
            conn_fn=conn_fn,
            create_table_fn=named_partial(
                fn=create_table,
                name=f"exportation_create_{table.name}",
                table=table,
            ),
            wait_for=wait_tasks,
        )

        bootstrap_future = task_open_bucket_operation.submit(
            conn_fn=conn_fn,
            settings=bucket_settings,
            bucket_operation_fn=named_partial(
                fn=bootstrap_table,
                name=f"exportation_bootstrap_{table.name}",
                domain=domain,
                table=table,
            ),
            secret_label=table.name,
            wait_for=[create_table_future],
        )

        upsert_future = task_open_bucket_operation.submit(
            conn_fn=conn_fn,
            settings=bucket_settings,
            bucket_operation_fn=named_partial(
                fn=upsert_fn,
                name=f"exportation_upsert_{table.name}",
                catalog=catalog,
            ),
            secret_label=table.name,
            wait_for=[bootstrap_future],
        )

        asset_futures[table.name] = upsert_future

    for future in asset_futures.values():
        future.result()
