from functools import partial
from pathlib import Path
from typing import Optional

import duckdb

from src.persistence.database.operation import execute_query
from src.persistence.storage import BucketSettings
from src.persistence.storage.utils import set_path
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)

BASE_STORAGE_PATH = Path(
    "acidentes",
    "gold",
    "agg_letalidade_pista_clima",
).as_posix()
set_storage_path = partial(
    set_path,
    base_path=BASE_STORAGE_PATH,
)

DIM_STORAGE_BASE_PATH = Path(
    "acidentes",
    "silver",
).as_posix()
set_dim_storage_path = partial(
    set_path,
    base_path=DIM_STORAGE_BASE_PATH,
)


def bootstrap_table(
    conn: duckdb.DuckDBPyConnection,
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script bootstrap_table.sql"""
    try:
        execute_query(
            conn=conn,
            query_key="bootstrap_table",
            query_dict=QUERIES,
            storage_path=set_storage_path(settings=settings),
        )
    except duckdb.IOException:
        pass


def copy_to_parquet(
    conn: duckdb.DuckDBPyConnection,
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script copy_to_parquet.sql"""
    execute_query(
        conn=conn,
        query_key="copy_to_parquet",
        query_dict=QUERIES,
        storage_path=set_storage_path(settings=settings),
    )


def create_table(conn: duckdb.DuckDBPyConnection):
    """Delega a execução do script create_table.sql"""
    execute_query(
        conn=conn,
        query_key="create_table",
        query_dict=QUERIES,
    )


def upsert_table(
    conn: duckdb.DuckDBPyConnection,
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script upsert_table.sql"""
    dim_storage_path = {
        "dim_local_storage_path": Path(
            set_dim_storage_path(settings=settings),
            "dim_local",
        ).as_posix(),
        "dim_pista_storage_path": Path(
            set_dim_storage_path(settings=settings),
            "dim_pista",
        ).as_posix(),
        "dim_clima_storage_path": Path(
            set_dim_storage_path(settings=settings),
            "dim_clima",
        ).as_posix(),
        "dim_categoria_storage_path": Path(
            set_dim_storage_path(settings=settings),
            "dim_categoria",
        ).as_posix(),
    }

    execute_query(
        conn=conn,
        query_key="upsert_table",
        query_dict=QUERIES,
        **dim_storage_path,
    )
