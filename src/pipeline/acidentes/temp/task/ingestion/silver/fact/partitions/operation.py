from typing import Callable, Optional, ContextManager

import duckdb
from prefect import task

from src.persistence.storage.settings import BucketSettings
from src.persistence.database.operation import execute
from .constants.sql import (
    CREATE_TEMP_QUERIES_SQL,
    UPSERT_TEMP_QUERIES_SQL,
    UPSERT_FT_QUERIES_SQL,
)
from ...staging.utils.storage import set_storage_path


@task(
    name="create_temp_table",
    task_run_name="create_temp_table: {target_table}",
)
def create_temp_table(
    target_table: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
):
    """Delega a execução do script de create_temp"""
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=CREATE_TEMP_QUERIES_SQL[target_table],
        )


@task(
    name="upsert_ft_table",
    task_run_name="upsert_ft_table: {target_table}",
)
def upsert_ft_table(
    target_table: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
):
    """Delega a execução do script de upsert_ft"""
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=UPSERT_FT_QUERIES_SQL[target_table],
        )


@task(
    name="upsert_temp_table",
    task_run_name="upsert_temp_table: {partition_values}",
)
def upsert_temp_table(
    target_table: str,
    source_table: str,
    partition_values: str,
    filter_clause: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script de upsert_temp"""
    with conn_fn() as conn:
        execute(
            conn=conn,
            partition_values=partition_values,
            filter_clause=filter_clause,
            query=UPSERT_TEMP_QUERIES_SQL[target_table],
            staging_storage_path=set_storage_path(
                table_name=source_table,
                settings=settings,
            ),
        )
