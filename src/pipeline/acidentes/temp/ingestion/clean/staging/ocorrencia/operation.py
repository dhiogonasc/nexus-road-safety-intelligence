from typing import Callable, Optional, ContextManager

import duckdb
from prefect import task

from src.persistence.storage.settings import BucketSettings
from src.persistence.database.operation import execute_query
from src.shared.system.file import load_module_queries
from .storage import (
    set_storage_path,
    set_log_path,
    set_raw_storage_path,
    set_raw_log_path,
)

QUERIES = load_module_queries(current_file=__file__)


@task(
    name="stage",
    task_run_name="stage: ocorrencias",
)
def stage(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script stage.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="stage",
            query_dict=QUERIES,
            raw_storage_path=set_raw_storage_path(settings=settings),
            raw_log_path=set_raw_log_path(settings=settings),
        )


@task(
    name="copy_to_parquet",
    task_run_name="copy_to_parquet: ocorrencias",
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
    name="log_charge",
    task_run_name="log_charge: ocorrencias",
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
