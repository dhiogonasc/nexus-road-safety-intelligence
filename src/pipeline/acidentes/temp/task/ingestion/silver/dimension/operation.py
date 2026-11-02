from typing import Callable, ContextManager, Optional

import duckdb
from prefect import task

from src.persistence.database.operation import execute
from src.persistence.storage.settings import BucketSettings
from .utils.storage import set_storage_path
from .constants.sql import (
    BOOTSTRAP_QUERIES_SQL,
    COPY_TO_PARQUET_QUERIES_SQL,
    CREATE_QUERIES_SQL,
    UPSERT_QUERIES_SQL,
)


@task(
    name="create_table",
    task_run_name="create_table: {table_name}",
)
def create_table(
    table_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
):
    """Delega a execução do script de create"""
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=CREATE_QUERIES_SQL[table_name],
        )


@task(
    name="bootstrap_table",
    task_run_name="bootstrap_table: {table_name}",
)
def bootstrap_table(
    table_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script de bootstrap"""
    with conn_fn() as conn:
        try:
            execute(
                conn=conn,
                query=BOOTSTRAP_QUERIES_SQL[table_name],
                storage_path=set_storage_path(
                    table_name=table_name,
                    settings=settings,
                ),
            )
        except duckdb.IOException:
            pass


@task(
    name="upsert_table",
    task_run_name="upsert_table: {table_name}",
)
def upsert_table(
    table_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
):
    """Delega a execução do script de upsert"""
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=UPSERT_QUERIES_SQL[table_name],
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
