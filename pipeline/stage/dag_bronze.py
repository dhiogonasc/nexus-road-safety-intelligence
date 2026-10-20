"""pipeline/stage/dag_bronze.py"""

from functools import partial
from prefect import flow

from config import settings, bucket_settings
from src.shared.db.operation import load_extensions
from src.shared.system.cmd import declare_domain
from src.shared.db.connection import create_connection
from src.pipeline.index import PIPELINE_CONFIG
from src.pipeline.bronze.extract import create_bronze_table_from_csv
from src.shared.pipeline.task import (
    task_create_schema,
    task_create_table,
)


def create_stage_table(
    domain: str,
    table: str,
    data_path,
):
    """Cria uma função parcialmente aplicada para a extração da tabela."""

    fn = partial(
        create_bronze_table_from_csv,
        settings=bucket_settings,
        domain=domain,
        table=table,
        csv_path=data_path,
    )
    fn.__name__ = f"create_stage_{table}"
    return fn


@flow(
    name="Bronze",
    flow_run_name="flow_bronze: {domain}",
)
def flow_bronze(
    database: str,
    domain: str,
) -> None:
    """Orquestra o processamento bronze para um dominio e banco duckdb dedicado"""

    pipeline_domain = PIPELINE_CONFIG[domain]
    pipeline_stage = "bronze"
    bronze_tables = pipeline_domain[pipeline_stage]

    load_extension = partial(
        load_extensions,
        extensions=[
            "httpfs",
            "parquet",
        ],
    )
    conn_fn = partial(
        create_connection,
        load_extensions_fn=load_extension,
        database=database,
    )
    schema_future = task_create_schema(
        schema=pipeline_stage,
        conn_fn=conn_fn,
    )

    table_futures = []
    for table, data_path in bronze_tables.items():
        create_table_fn = create_stage_table(
            domain=domain,
            table=table,
            data_path=data_path,
        )
        future = task_create_table.submit(
            conn_fn=conn_fn,
            create_table_fn=create_table_fn,
            wait_for=[schema_future],
        )
        table_futures.append(future)

    for future in table_futures:
        future.result()


if __name__ == "__main__":
    args = declare_domain()

    DOMAIN = args.domain
    DATABASE = settings.domain_db_path(domain=DOMAIN)

    flow_bronze(
        database=DATABASE,
        domain=DOMAIN,
    )
