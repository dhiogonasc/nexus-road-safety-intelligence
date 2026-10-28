from functools import partial
from pathlib import Path
from typing import Optional

import duckdb

from src.persistence.database.operation import execute_query
from src.persistence.storage import BucketSettings
from src.persistence.storage.utils import set_path
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)

BASE_STORAGE_PATH = Path("acidentes", "silver", "ft_ocorrencia").as_posix()
set_storage_path = partial(
    set_path,
    base_path=BASE_STORAGE_PATH,
)


def bootstrap(
    conn: duckdb.DuckDBPyConnection,
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script bootstrap.sql"""
    try:
        execute_query(
            conn=conn,
            query_key="bootstrap",
            query_dict=QUERIES,
            storage_path=set_storage_path(settings=settings),
        )
    except duckdb.IOException:
        pass


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
    for uf in _fetch_partition(conn=conn):
        execute_query(
            conn=conn,
            query_key="upsert",
            query_dict=QUERIES,
            uf=uf
        )


def _fetch_partition(conn: duckdb.DuckDBPyConnection):
    """
    Delega a execução do script fetch_partition.sql
    e retorna uma lista de valores para partição.
    """
    partitions = execute_query(
        conn=conn,
        query_key="fetch_partition",
        query_dict=QUERIES,
    ).fetchall()

    return [partition_row[0] for partition_row in partitions]
