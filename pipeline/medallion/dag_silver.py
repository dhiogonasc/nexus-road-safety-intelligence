from functools import partial
from typing import Callable
from prefect import flow, task

from settings import BucketSettings, bucket_settings
from src.shared.utils.fn import named_partial
from src.shared.db.operation import (
    bootstrap_table,
    copy_table_to_parquet,
    create_table,
    load_extensions,
)
from src.shared.db.connection import create_connection
from src.pipeline.index import PIPELINE_CONFIG
from src.pipeline.acidentes.silver.operation import fetch_last_charged
from src.shared.pipeline.task import (
    task_create_schema,
    task_create_table,
    task_open_bucket_operation,
)


@flow(
    name="Silver",
    flow_run_name="flow_silver: {domain}",
)
def flow_silver(
    database: str,
    domain: str,
) -> None:
    """Orquestra o processamento silver para um dominio e banco duckdb dedicado"""

    domain_pipeline_config = PIPELINE_CONFIG.get_domain_config(domain=domain)
    assets = domain_pipeline_config.silver

    load_extensions_fn = partial(
        load_extensions,
        extensions=[
            "httpfs",
            "parquet",
        ],
    )
    conn_fn = partial(
        create_connection,
        load_extensions_fn=load_extensions_fn,
        database=database,
    )

    schema_future = task_create_schema.submit(
        conn_fn=conn_fn,
        schema="silver",
    )
    last_charge_future = task_open_bucket_operation.submit(
        conn_fn=conn_fn,
        settings=bucket_settings,
        bucket_operation_fn=load_last_charge_fn,
        secret_label=table.name,
        wait_for=[bootstrap_future],
    )

    asset_futures = {}

    for asset in assets:
        wait_tasks = [last_charge_future]

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
                name=f"create_{table.name}",
                table=table,
            ),
            wait_for=wait_tasks,
        )

        bootstrap_future = task_open_bucket_operation.submit(
            conn_fn=conn_fn,
            settings=bucket_settings,
            bucket_operation_fn=named_partial(
                fn=bootstrap_table,
                name=f"bootstrap_{table.name}",
                domain=domain,
                table=table,
            ),
            secret_label=table.name,
            wait_for=[create_table_future],
        )

        upsert_future = task_open_bucket_operation.submit(
            conn_fn=conn_fn,
            settings=bucket_settings,
            bucket_operation_fn=upsert_fn,
            secret_label=table.name,
            wait_for=[bootstrap_future],
        )

        copy_future = task_open_bucket_operation.submit(
            conn_fn=conn_fn,
            settings=bucket_settings,
            bucket_operation_fn=named_partial(
                fn=copy_table_to_parquet,
                name=f"copy_{table.name}_to_parquet",
                domain=domain,
                table=table,
            ),
            secret_label=table.name,
            wait_for=[upsert_future],
        )

        asset_futures[table.name] = copy_future

    for future in asset_futures.values():
        future.result()
