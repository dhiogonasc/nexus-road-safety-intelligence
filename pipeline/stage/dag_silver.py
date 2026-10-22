from functools import partial
from prefect import flow

from config import settings, bucket_settings
from src.shared.db.operation import bootstrap_table, copy_table_to_parquet, create_table
from src.shared.system.cmd import declare_domain
from src.shared.db.connection import create_connection
from src.pipeline.index import PIPELINE_CONFIG
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

    pipeline_stage = "silver"
    pipeline_domain = PIPELINE_CONFIG[domain]
    silver_assets = pipeline_domain[pipeline_stage]

    conn_fn = partial(
        create_connection,
        database=database,
    )
    schema_future = task_create_schema.submit(
        conn_fn=conn_fn,
        schema=pipeline_stage,
    )

    asset_futures = {}

    for asset in silver_assets:
        wait_tasks = [schema_future]

        table = asset.table
        upsert_fn = asset.upsert_fn
        depends_on = asset.depends_on

        for dependency in depends_on:
            if dependency.table.name in asset_futures:
                wait_tasks.append(asset_futures[dependency.table.name])

        create_table_future = task_create_table.submit(
            conn_fn=conn_fn,
            create_table_fn=partial(
                create_table,
                table=table,
            ),
            wait_for=wait_tasks,
        )

        bootstrap_future = task_open_bucket_operation.submit(
            conn_fn=conn_fn,
            settings=bucket_settings,
            bucket_operation_fn=partial(
                bootstrap_table,
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
            bucket_operation_fn=partial(
                copy_table_to_parquet,
                domain=domain,
                table=table,
            ),
            secret_label=table.name,
            wait_for=[upsert_future],
        )

        asset_futures[table.name] = copy_future

    for future in asset_futures.values():
        future.result()


if __name__ == "__main__":
    args = declare_domain()

    DOMAIN = args.domain
    DATABASE = settings.domain_db_path(domain=DOMAIN)

    flow_silver(
        database=DATABASE,
        domain=DOMAIN,
    )
