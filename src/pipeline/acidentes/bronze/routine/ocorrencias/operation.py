from pathlib import Path
from typing import Callable, ContextManager, Optional

import duckdb
from prefect import task

from constants import AC_OCORRENCIAS_DIR
from src.persistence.storage.settings import BucketSettings
from src.persistence.database.operation import execute_query
from src.shared.system.file import load_module_queries
from .storage import set_storage_path, set_log_path

QUERIES = load_module_queries(current_file=__file__)

SOURCE_PATH = Path(AC_OCORRENCIAS_DIR, "*.csv").as_posix()


@task(
    name="Create Table",
    task_run_name="raw_ocorrencias: create_table",
)
def create_table(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    delim: str = ";",
    encoding: str = "latin-1",
):
    """Delega a execução do script create_table.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="create_table",
            query_dict=QUERIES,
            csv_path=SOURCE_PATH,
            delim=delim,
            encoding=encoding,
        )


@task(
    name="Copy Table to Parquet",
    task_run_name="raw_ocorrencias: copy_to_parquet",
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
    name="Log Table Charge",
    task_run_name="raw_ocorrencias: log_charge",
)
def log_charge(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script log_charge.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="log_charge",
            query_dict=QUERIES,
            log_path=set_log_path(settings=settings),
        )


@task(
    name="Process Table Routine",
    task_run_name="raw_ocorrencias: process_routine",
)
def process_routine(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    create_future = create_table.submit(conn_fn=conn_fn)

    futures = []

    copy_future = copy_to_parquet.submit(
        conn_fn=conn_fn,
        settings=settings,
        wait_for=[create_future],
    )
    futures.append(copy_future)

    log_future = log_charge.submit(
        conn_fn=conn_fn,
        settings=settings,
        wait_for=[create_future],
    )
    futures.append(log_future)

    for future in futures:
        future.result()
