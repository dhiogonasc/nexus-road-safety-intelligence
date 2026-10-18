from functools import partial
from prefect import flow, task

from config import settings
from src.pipeline.index import PIPELINE_CONFIG
from src.pipeline.gold.merge import export_aggregation
from src.shared.pipeline.task import task_create_schema, task_create_table_from_fn
from src.shared.db.connection import create_connection
from src.shared.db.operation import (
    attach_connections,
    load_extensions,
)
from src.shared.system.cmd import run_flow


@task(
    name="Sync Gold",
    task_run_name="task_export_table: {table_config[target]}",
)
def task_export_table(
    database: str,
    schema: str,
    table: str,
    table_config: dict,
) -> None:
    """Consolida a criação de tabelas na entidade de persistencia dedicada"""

    catalog = f"pg_rsi_pei6_{table}"
    load_postgres_extension = partial(
        load_extensions,
        extensions=["postgres"],
    )
    attach_postgres = partial(
        attach_connections,
        connections=[
            {
                "conn_string": settings.postgres_conn_string,
                "conn_alias": catalog,
                "conn_option": "(TYPE POSTGRES)",
            }
        ],
    )
    with create_connection(
        database=database,
        load_extensions_fn=load_postgres_extension,
        attach_connections_fn=attach_postgres,
    ) as conn:
        export_aggregation(
            source_schema="gold",
            source_table=table,
            target_catalog=catalog,
            target_schema="analytics",
            target_table=table_config["target"],
            primary_keys=table_config["primary_keys"],
            conn=conn,
        )


@flow(name="Gold", flow_run_name="flow_gold: {domain}")
def flow_gold(database: str, domain: str) -> None:
    """Orquestra o processamento gold para um dominio e persistência dedicada"""

    pipeline_domain = PIPELINE_CONFIG[domain]
    pipeline_stage = "gold"
    gold_tables = pipeline_domain[pipeline_stage]

    schema_future = task_create_schema.submit(
        database=database,
        schema_name=pipeline_stage,
    )
    schema_future.result()

    create_futures = {}
    export_futures = []

    for table, table_config in gold_tables.items():
        create_future = task_create_table_from_fn.submit(
            database=database,
            create_table_fn=table_config["fn"],
            wait_for=[schema_future],
        )
        create_futures[table] = create_future

    for table, table_config in gold_tables.items():
        export_future = task_export_table.submit(
            database=database,
            schema=domain,
            table=table,
            table_config=table_config,
            wait_for=[create_futures[table]],
        )
        export_futures.append(export_future)

    for export_future in export_futures:
        export_future.result()


if __name__ == "__main__":
    run_flow(flow_factory=flow_gold)
