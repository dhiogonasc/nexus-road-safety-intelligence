from duckdb import IOException
from prefect import task

from .constants.sql import (
    BOOTSTRAP_QUERIES_SQL,
    COPY_TO_PARQUET_QUERIES_SQL,
    CREATE_QUERIES_SQL,
    UPSERT_QUERIES_SQL,
)
from .constants.storage import BASE_PATH
from src.persistence.database.provider import DuckDBProvider
from src.persistence.storage.provider import StorageProvider


@task(
    name="bootstrap_table",
    task_run_name="bootstrap_table: {table}",
)
def bootstrap_table(
    table: str,
    duckdb: DuckDBProvider,
    storage: StorageProvider,
):
    try:
        return duckdb.execute_query(
            sql=BOOTSTRAP_QUERIES_SQL[table],
            storage_path=storage.get_storage_path(),
        )
    except IOException:
        pass


@task(
    name="copy_table_to_parquet",
    task_run_name="copy_table_to_parquet: {table}",
)
def copy_table_to_parquet(
    table: str,
    duckdb: DuckDBProvider,
    storage: StorageProvider,
):
    return duckdb.execute_query(
        sql=COPY_TO_PARQUET_QUERIES_SQL[table],
        storage_path=storage.get_storage_path(),
    )


@task(
    name="create_table",
    task_run_name="create_table: {table}",
)
def create_table(
    table: str,
    duckdb: DuckDBProvider,
):
    return duckdb.execute_query(sql=CREATE_QUERIES_SQL[table])


@task(
    name="dimension_storage_factory",
    task_run_name="dimension_storage_factory: {table}",
)
def dimension_storage_factory(table: str):
    return StorageProvider(
        table_name=table,
        base_path=BASE_PATH,
    )


@task(
    name="upsert_table",
    task_run_name="upsert_table: {table}",
)
def upsert_table(
    table: str,
    duckdb: DuckDBProvider,
):
    return duckdb.execute_query(sql=UPSERT_QUERIES_SQL[table])
