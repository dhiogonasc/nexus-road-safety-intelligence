from typing import Callable, ContextManager, Optional, Dict

import duckdb
from prefect import task

from src.persistence.storage.settings import BucketSettings
from src.persistence.database.operation import execute
from .constants.sql import (
    STAGE_QUERIES_SQL,
    LOG_CHARGE_QUERIES_SQL,
    COPY_TO_PARQUET_QUERIES_SQL,
)
from .utils.storage import (
    set_storage_path,
    set_log_path,
)
from ...silver.fact.utils.storage import (
    set_storage_path as set_source_storage_path,
)


@task(
    name="stage_table",
    task_run_name="stage_table: {target_table}",
)
def stage_table(
    source_table: str,
    target_table: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script de stage"""
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=STAGE_QUERIES_SQL[target_table],
            source_storage_path=set_source_storage_path(
                table_name=source_table,
                settings=settings,
            ),
        )


@task(
    name="copy_table_to_parquet",
    task_run_name="copy_table_to_parquet: {target_table}",
)
def copy_table_to_parquet(
    target_table: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script de copy_to_parquet"""
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=COPY_TO_PARQUET_QUERIES_SQL[target_table],
            storage_path=set_storage_path(
                table_name=target_table,
                settings=settings,
            ),
        )


@task(
    name="log_table_charge",
    task_run_name="log_table_charge: {target_table}",
)
def log_table_charge(
    target_table: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script de log_charge"""
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=LOG_CHARGE_QUERIES_SQL[target_table],
            log_path=set_log_path(
                table_name=target_table,
                settings=settings,
            ),
        )
