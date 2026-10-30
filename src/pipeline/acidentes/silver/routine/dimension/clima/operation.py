from functools import partial
from pathlib import Path
from typing import Callable, Optional, ContextManager

import duckdb
from prefect import task

from src.persistence.storage import BucketSettings
from src.persistence.storage.utils import set_path
from src.persistence.database.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)

STORAGE_PATH = Path(
    "acidentes",
    "silver",
    "dimension",
    "clima",
).as_posix()
set_storage_path = partial(
    set_path,
    base_path=STORAGE_PATH,
)


@task(
    name="create_table",
    task_run_name="dim_clima: create_table",
)
def create_table(conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]]):
    """Delega a execução do script create_table.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="create_table",
            query_dict=QUERIES,
        )


@task(
    name="bootstrap_table",
    task_run_name="dim_clima: bootstrap_table",
)
def bootstrap_table(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script bootstrap_table.sql"""
    with conn_fn() as conn:
        try:
            execute_query(
                conn=conn,
                query_key="bootstrap_table",
                query_dict=QUERIES,
                storage_path=set_storage_path(settings=settings),
            )
        except duckdb.IOException:
            pass


@task(
    name="upsert_table",
    task_run_name="dim_clima: upsert_table",
)
def upsert_table(conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]]):
    """Delega a execução do script upsert_table.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="upsert_table",
            query_dict=QUERIES,
        )


@task(
    name="copy_to_parquet",
    task_run_name="dim_clima: copy_to_parquet",
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


@task(
    name="process_routine",
    task_run_name="dim_clima: process_routine",
)
def process_routine(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    create_future = create_table.submit(conn_fn=conn_fn)

    bootstrap_future = bootstrap_table.submit(
        conn_fn=conn_fn,
        settings=settings,
        wait_for=[create_future],
    )

    upsert_future = upsert_table.submit(
        conn_fn=conn_fn,
        wait_for=[bootstrap_future],
    )

    copy_future = copy_to_parquet.submit(
        conn_fn=conn_fn,
        settings=settings,
        wait_for=[upsert_future],
    )
    copy_future.result()
