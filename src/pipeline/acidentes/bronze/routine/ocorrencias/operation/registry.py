from functools import partial
from pathlib import Path
from typing import Optional

import duckdb

from constants import BASE_DIR
from persistence.storage.utils import set_path
from settings import BucketSettings
from src.persistence.database.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)

BASE_STORAGE_PATH = Path("acidentes", "bronze", "ocorrencias")
BASE_LOG_PATH = Path("acidentes", "bronze", "log", "ocorrencias")

set_storage_path = partial(
    set_path,
    base_path=BASE_STORAGE_PATH,
)

set_log_path = partial(
    set_path,
    base_path=BASE_LOG_PATH,
)


def create(
    conn: duckdb.DuckDBPyConnection,
    csv_path: str,
    delim: str = ";",
    encoding: str = "latin-1",
):
    """Delega a execução do script create.sql"""
    execute_query(
        conn=conn,
        query_key="create",
        query_dict=QUERIES,
        csv_path=csv_path,
        delim=delim,
        encoding=encoding,
    )


def copy(
    conn: duckdb.DuckDBPyConnection,
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script copy.sql"""
    execute_query(
        conn=conn,
        query_key="copy",
        query_dict=QUERIES,
        storage_path=set_storage_path(settings=settings),
    )


def log(
    conn: duckdb.DuckDBPyConnection,
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script log.sql"""
    execute_query(
        conn=conn,
        query_key="log",
        query_dict=QUERIES,
        storage_path=set_storage_path(settings=settings),
        log_path=set_log_path(settings=settings),
    )
