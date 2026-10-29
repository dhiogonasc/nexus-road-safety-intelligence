from functools import partial
from pathlib import Path
from typing import Callable, Optional

import duckdb
from prefect import task

from constants import AC_OCORRENCIAS_DIR
from src.persistence.storage import BucketSettings
from src.persistence.storage.utils import set_path
from src.persistence.database.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)

SOURCE_PATH = Path(AC_OCORRENCIAS_DIR, "*.csv").as_posix()

BASE_STORAGE_PATH = Path(
    "acidentes",
    "bronze",
    "raw_ocorrencias",
)
set_storage_path = partial(
    set_path,
    base_path=BASE_STORAGE_PATH,
)

BASE_LOG_PATH = Path(
    "acidentes",
    "bronze",
    "log",
    "raw_ocorrencias",
)
set_log_path = partial(
    set_path,
    base_path=BASE_LOG_PATH,
)


@task(
    name="Create Table",
    task_run_name="create raw_ocorrencias",
)
def create_table(
    conn_fn: Callable,
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
    task_run_name="copy raw_ocorrencias to parquet",
)
def copy_to_parquet(
    conn_fn: Callable,
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
    task_run_name="log raw_ocorrencias charge",
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
            storage_path=set_storage_path(settings=settings),
            log_path=set_log_path(settings=settings),
        )


@task(
    name="Process Table Routine",
    task_run_name="process raw_ocorrencias routine",
)
def process_routine(
    conn_fn: Callable,
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
