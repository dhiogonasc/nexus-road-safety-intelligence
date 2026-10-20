"""pipeline/stage/dag_bronze.py"""

from functools import partial
import duckdb
from prefect import flow, task

from config import settings
from src.shared.db.operation import load_extensions
from src.shared.system.cmd import declare_domain
from src.shared.db.connection import create_connection
from src.pipeline.index import PIPELINE_CONFIG
from src.pipeline.bronze.extract import (
    create_bucket_secret,
    create_bronze_table_from_csv,
    copy_bronze_table_to_parquet,
)
from src.shared.pipeline.task import (
    task_create_schema,
    task_create_table,
)


def create_stage_table(table: str, data_path):
    """Cria uma função parcialmente aplicada para a extração da tabela."""

    fn = partial(
        create_bronze_table_from_csv,
        table=table,
        csv_path=data_path,
    )
    fn.__name__ = f"create_stage_{table}"
    return fn


@task(
    name="Copy Table To Parquet",
    task_run_name="task_copy_table_to_parquet: {domain}/{table}",
)
def task_copy_table_to_parquet(
    conn_fn: duckdb.DuckDBPyConnection,
    domain: str,
    table: str,
    bucket_name: str,
    secret_name: str,
    storage_access_key_id: str,
    storage_secret_access_key: str,
    storage_region: str,
    storage_endpoint: str,
):
    """Consolida a copia da tabela em parquet"""
    with conn_fn() as conn:
        create_bucket_secret(
            conn=conn,
            secret_name=secret_name,
            storage_access_key_id=storage_access_key_id,
            storage_secret_access_key=storage_secret_access_key,
            storage_region=storage_region,
            storage_endpoint=storage_endpoint,
        )

        copy_bronze_table_to_parquet(
            conn=conn,
            domain=domain,
            table=table,
            bucket_name=bucket_name,
        )


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

    copy_futures = []
    for table, data_path in bronze_tables.items():
        create_table_fn = create_stage_table(
            table=table,
            data_path=data_path,
        )
        table_future = task_create_table(
            conn_fn=conn_fn,
            create_table_fn=create_table_fn,
            wait_for=[schema_future],
        )
        copy_future = task_copy_table_to_parquet.submit(
            conn_fn=conn_fn,
            bucket_name=settings.STORAGE_BUCKET,
            domain=domain,
            table=table,
            secret_name=f"{table}_{settings.STORAGE_BUCKET}",
            storage_access_key_id=settings.STORAGE_ACCESS_KEY_ID,
            storage_secret_access_key=settings.STORAGE_SECRET_ACCESS_KEY,
            storage_region=settings.STORAGE_REGION,
            storage_endpoint=settings.STORAGE_ENDPOINT,
            wait_for=[table_future],
        )
        copy_futures.append(copy_future)

    for future in copy_futures:
        future.result()


if __name__ == "__main__":
    args = declare_domain()

    DOMAIN = args.domain
    DATABASE = settings.domain_db_path(domain=DOMAIN)

    flow_bronze(
        database=DATABASE,
        domain=DOMAIN,
    )
