from functools import partial
from pathlib import Path
from typing import Optional

import duckdb

from settings import BucketSettings
from src.persistence.database.operation import execute_query
from src.persistence.storage.utils import set_path
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)

BASE_STORAGE_PATH = Path("acidentes", "silver", "dim_localizacao").as_posix()
set_storage_path = partial(
    set_path,
    base_path=BASE_STORAGE_PATH,
)


def bootstrap(
    conn: duckdb.DuckDBPyConnection,
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script bootstrap.sql"""
    execute_query(
        conn=conn,
        query_key="bootstrap",
        query_dict=QUERIES,
        storage_path=set_storage_path(settings=settings),
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


def create(conn: duckdb.DuckDBPyConnection):
    """Delega a execução do script create.sql"""
    execute_query(
        conn=conn,
        query_key="create",
        query_dict=QUERIES,
    )


def upsert(conn: duckdb.DuckDBPyConnection):
    """Delega a execução do script upsert.sql"""
    execute_query(
        conn=conn,
        query_key="upsert",
        query_dict=QUERIES,
    )
