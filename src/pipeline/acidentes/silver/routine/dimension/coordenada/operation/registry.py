from pathlib import Path
from typing import Optional

import duckdb

from constants import BASE_DIR
from settings import BucketSettings
from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def _set_storage_path(settings: Optional[BucketSettings] = None) -> str:
    base_path = Path("acidentes", "silver", "dim_coordenada").as_posix()
    if settings:
        storage_path = Path(f"s3://{settings.STORAGE_BUCKET}", base_path).as_posix()
    else:
        storage_path = Path(BASE_DIR, base_path).as_posix()
    return storage_path


def bootstrap(
    conn: duckdb.DuckDBPyConnection,
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script bootstrap.sql"""
    storage_path = _set_storage_path(settings=settings)

    execute_query(
        conn=conn,
        query_key="bootstrap",
        query_dict=QUERIES,
        storage_path=storage_path,
    )


def copy(
    conn: duckdb.DuckDBPyConnection,
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script copy.sql"""
    storage_path = _set_storage_path(settings=settings)

    execute_query(
        conn=conn,
        query_key="copy",
        query_dict=QUERIES,
        storage_path=storage_path,
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
