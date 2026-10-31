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
    name="stage",
    task_run_name="stage: raw_ocorrencias",
)
def stage(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    delim: str = ";",
    encoding: str = "latin-1",
):
    """Delega a execução do script stage.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="stage",
            query_dict=QUERIES,
            csv_path=SOURCE_PATH,
            delim=delim,
            encoding=encoding,
        )

@task(
    name="copy_to_parquet",
    task_run_name="copy_to_parquet: raw_ocorrencias",
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
    task_run_name="log_charge: raw_ocorrencias",
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
