from functools import partial
from pathlib import Path
from typing import Optional

import duckdb

from src.persistence.database.operation import execute_query
from src.persistence.storage import BucketSettings
from src.persistence.storage.utils import set_path
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)

BASE_STORAGE_PATH = Path("acidentes", "gold", "agg_letalidade_pista_clima").as_posix()
set_storage_path = partial(
    set_path,
    base_path=BASE_STORAGE_PATH,
)

DIM_STORAGE_BASE_PATH = Path("acidentes", "silver").as_posix()
set_dim_storage_path = partial(
    set_path,
    base_path=DIM_STORAGE_BASE_PATH,
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


def upsert(
    conn: duckdb.DuckDBPyConnection,
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script upsert.sql"""
    dim_storage_path = {
        "dim_localizacao_storage_path": Path(
            set_dim_storage_path(settings=settings),
            "dim_localizacao",
        ).as_posix(),
        "dim_pista_storage_path": Path(
            set_dim_storage_path(settings=settings),
            "dim_pista",
        ).as_posix(),
        "dim_condicao_metereologica_storage_path": Path(
            set_dim_storage_path(settings=settings),
            "dim_condicao_metereologica",
        ).as_posix(),
        "dim_causa_storage_path": Path(
            set_dim_storage_path(settings=settings),
            "dim_causa",
        ).as_posix(),
        "dim_tipo_storage_path": Path(
            set_dim_storage_path(settings=settings),
            "dim_tipo",
        ).as_posix(),
        "dim_classificacao_storage_path": Path(
            set_dim_storage_path(settings=settings),
            "dim_classificacao",
        ).as_posix(),
    }

    execute_query(
        conn=conn,
        query_key="upsert",
        query_dict=QUERIES,
        **dim_storage_path,
    )
