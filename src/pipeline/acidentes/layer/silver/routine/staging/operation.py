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
    "stg",
).as_posix()
set_storage_path = partial(
    set_path,
    base_path=STORAGE_PATH,
)

LOG_PATH = Path(
    "acidentes",
    "silver",
    "log",
    "stg",
).as_posix()
set_log_path = partial(
    set_path,
    base_path=LOG_PATH,
)

RAW_STORAGE_PATH = Path(
    "acidentes",
    "bronze",
    "raw_ocorrencias",
).as_posix()
set_raw_storage_path = partial(
    set_path,
    base_path=RAW_STORAGE_PATH,
)

RAW_LOG_PATH = Path(
    "acidentes",
    "bronze",
    "log",
    "raw_ocorrencias",
).as_posix()
set_raw_log_path = partial(
    set_path,
    base_path=RAW_LOG_PATH,
)


@task(
    name="create_table",
    task_run_name="stg: create_table",
)
def create_table(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script create_table.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="create_table",
            query_dict=QUERIES,
            raw_storage_path=set_raw_storage_path(settings=settings),
            raw_log_path=set_raw_log_path(settings=settings),
        )


@task(
    name="copy_to_parquet",
    task_run_name="stg: copy_to_parquet",
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
    task_run_name="stg: log_charge",
)
def log_charge(
    conn_fn: Callable,
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
    name="process_routine",
    task_run_name="stg: process_routine",
)
def process_routine(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script create_table.sql"""
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
