from prefect import task

from .constants.sql import (
    STAGE_QUERIES_SQL,
    LOG_CHARGE_QUERIES_SQL,
    COPY_TO_PARQUET_QUERIES_SQL,
)
from .constants.storage import BASE_PATH
from .constants.summary import StagingTable
from src.persistence.database.provider import DuckDBProvider
from src.persistence.storage.provider import StorageProvider


@task(
    name="copy_table_to_parquet",
    task_run_name="copy_table_to_parquet: {table.name}",
)
def copy_table_to_parquet(
    table: StagingTable,
    storage: StorageProvider,
    duckdb: DuckDBProvider,
):
    duckdb.execute_query(
        sql=COPY_TO_PARQUET_QUERIES_SQL[table.name],
        storage_path=storage.get_storage_path(),
    )


@task(
    name="log_table_charge",
    task_run_name="log_table_charge: {table.name}",
)
def log_table_charge(
    table: StagingTable,
    storage: StorageProvider,
    duckdb: DuckDBProvider,
):
    duckdb.execute_query(
        sql=LOG_CHARGE_QUERIES_SQL[table.name],
        log_path=storage.get_log_path(),
    )


@task(
    name="staging_storage_factory",
    task_run_name="staging_storage_factory: {table.name}",
)
def staging_storage_factory(
    table: StagingTable,
):
    return StorageProvider(
        table_name=table.name,
        base_path=BASE_PATH,
    )


@task(
    name="stage_table",
    task_run_name="stage_table: {table.name}",
)
def stage_table(
    table: StagingTable,
    source_storage: StorageProvider,
    duckdb: DuckDBProvider,
):
    duckdb.execute_query(
        sql=STAGE_QUERIES_SQL[table.name],
        source_storage_path=source_storage.get_storage_path(),
        source_log_path=source_storage.get_log_path(),
    )
