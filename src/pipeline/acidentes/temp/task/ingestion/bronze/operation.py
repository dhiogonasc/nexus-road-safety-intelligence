from typing import Callable, ContextManager, Optional

import duckdb
from prefect import task

from src.persistence.storage.settings import BucketSettings
from src.persistence.database.operation import execute
from .constants.sql import (
    STAGE_QUERIES_SQL,
    LOG_CHARGE_QUERIES_SQL,
    COPY_TO_PARQUET_QUERIES_SQL,
)
from .constants.source import SOURCE_PATHS
from .utils.storage import (
    set_storage_path,
    set_log_path,
)


@task(
    name="stage_table",
    task_run_name="stage_table: {table_name}",
)
def stage_table(
    table_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    delim: str = ";",
    encoding: str = "latin-1",
):
    """Delega a execução do script de stage"""
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=STAGE_QUERIES_SQL[table_name],
            csv_path=SOURCE_PATHS[table_name],
            delim=delim,
            encoding=encoding,
        )


@task(
    name="log_table_charge",
    task_run_name="log_table_charge: {table_name}",
)
def log_table_charge(
    table_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script de log_charge"""
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=LOG_CHARGE_QUERIES_SQL[table_name],
            log_path=set_log_path(
                table_name=table_name,
                settings=settings,
            ),
        )


@task(
    name="copy_table_to_parquet",
    task_run_name="copy_table_to_parquet: {table_name}",
)
def copy_table_to_parquet(
    table_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script de copy_to_parquet"""
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=COPY_TO_PARQUET_QUERIES_SQL[table_name],
            storage_path=set_storage_path(
                table_name=table_name,
                settings=settings,
            ),
        )
