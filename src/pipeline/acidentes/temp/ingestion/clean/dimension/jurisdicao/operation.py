from typing import Callable, Optional, ContextManager

import duckdb
from prefect import task

from src.persistence.storage.settings import BucketSettings
from src.persistence.database.operation import execute_query
from src.shared.system.file import load_module_queries
from .storage import set_storage_path

QUERIES = load_module_queries(current_file=__file__)


@task(
    name="create",
    task_run_name="create: dim_jurisdicao",
)
def create(conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]]):
    """Delega a execução do script create.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="create",
            query_dict=QUERIES,
        )


@task(
    name="bootstrap",
    task_run_name="bootstrap: dim_jurisdicao",
)
def bootstrap(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script bootstrap.sql"""
    with conn_fn() as conn:
        try:
            execute_query(
                conn=conn,
                query_key="bootstrap",
                query_dict=QUERIES,
                storage_path=set_storage_path(settings=settings),
            )
        except duckdb.IOException:
            pass


@task(
    name="upsert",
    task_run_name="upsert: dim_jurisdicao",
)
def upsert(conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]]):
    """Delega a execução do script upsert.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="upsert",
            query_dict=QUERIES,
        )


@task(
    name="copy_to_parquet",
    task_run_name="copy_to_parquet: dim_jurisdicao",
)
def copy_to_parquet(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script copy_to_parquet.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="copy_to_parquet",
            query_dict=QUERIES,
            storage_path=set_storage_path(settings=settings),
        )
