from duckdb import IOException
from prefect import task

from .constants.sql import (
    BOOTSTRAP_QUERIES_SQL,
    COPY_TO_PARQUET_QUERIES_SQL,
    CREATE_QUERIES_SQL,
    UPSERT_QUERIES_SQL,
)
from .constants.summary import SilverDimensionTable
from src.persistence.database.provider import DuckDBProvider


@task(
    name="bootstrap_table",
    task_run_name="bootstrap_table: {table.name}",
)
def bootstrap_table(
    table: SilverDimensionTable,
    duckdb: DuckDBProvider,
):
    try:
        return duckdb.execute_query(
            sql=BOOTSTRAP_QUERIES_SQL[table.name],
            storage_path=table.storage.get_storage_path(),
        )
    except IOException:
        pass


@task(
    name="copy_table_to_parquet",
    task_run_name="copy_table_to_parquet: {table.name}",
)
def copy_table_to_parquet(
    table: SilverDimensionTable,
    duckdb: DuckDBProvider,
):
    return duckdb.execute_query(
        sql=COPY_TO_PARQUET_QUERIES_SQL[table.name],
        storage_path=table.storage.get_storage_path(),
    )


@task(
    name="create_table",
    task_run_name="create_table: {table.name}",
)
def create_table(
    table: SilverDimensionTable,
    duckdb: DuckDBProvider,
):
    return duckdb.execute_query(sql=CREATE_QUERIES_SQL[table.name])


@task(
    name="upsert_table",
    task_run_name="upsert_table: {table.name}",
)
def upsert_table(
    table: SilverDimensionTable,
    duckdb: DuckDBProvider,
):
    source_path = {
        f"{table.source.table_name}_storage_path": table.source.get_storage_path()
    }

    return duckdb.execute_query(
        sql=UPSERT_QUERIES_SQL[table.name],
        **source_path,
    )
