from prefect import task


from .constants.sql import (
    STAGE_QUERIES_SQL,
    LOG_CHARGE_QUERIES_SQL,
    COPY_TO_PARQUET_QUERIES_SQL,
)
from .constants.summary import BronzeTable
from src.persistence.database.provider import DuckDBProvider


@task(
    name="copy_table_to_parquet",
    task_run_name="copy_table_to_parquet: {table.name}",
)
def copy_table_to_parquet(
    table: BronzeTable,
    duckdb: DuckDBProvider,
):
    duckdb.execute_query(
        sql=COPY_TO_PARQUET_QUERIES_SQL[table.name],
        storage_path=table.storage.get_storage_path(),
    )


@task(
    name="log_table_charge",
    task_run_name="log_table_charge: {table.name}",
)
def log_table_charge(
    table: BronzeTable,
    duckdb: DuckDBProvider,
):
    duckdb.execute_query(
        sql=LOG_CHARGE_QUERIES_SQL[table.name],
        log_path=table.storage.get_log_path(),
    )


@task(
    name="stage_table",
    task_run_name="stage_table: {table.name}",
)
def stage_table(
    table: BronzeTable,
    duckdb: DuckDBProvider,
    delim: str = ";",
    encoding: str = "latin-1",
):
    duckdb.execute_query(
        sql=STAGE_QUERIES_SQL[table.name],
        source_data_path=table.source,
        delim=delim,
        encoding=encoding,
    )
