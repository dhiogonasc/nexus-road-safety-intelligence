from pathlib import Path
from typing import Optional

import duckdb

from constants import BASE_DIR
from settings import BucketSettings
from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def _set_storage_path(settings: Optional[BucketSettings] = None) -> str:
    base_path = Path("acidentes", "gold", "condicoes_via").as_posix()
    if settings:
        storage_path = Path(f"s3://{settings.STORAGE_BUCKET}", base_path).as_posix()
    else:
        storage_path = Path(BASE_DIR, base_path).as_posix()
    return storage_path


def _set_silver_storage_path(settings: Optional[BucketSettings] = None) -> dict:
    base_path = Path("acidentes", "silver", "dimension").as_posix()
    if settings:
        silver_storage_path = {
            "dim_tempo": Path(
                f"s3://{settings.STORAGE_BUCKET}",
                base_path,
                "dim_tempo",
                "dim_tempo.parquet",
            ).as_posix(),
            "dim_condicao_metereologica": Path(
                f"s3://{settings.STORAGE_BUCKET}",
                base_path,
                "dim_condicao_metereologica",
                "dim_condicao_metereologica.parquet",
            ).as_posix(),
            "dim_pista": Path(
                f"s3://{settings.STORAGE_BUCKET}",
                base_path,
                "dim_pista",
                "dim_pista.parquet",
            ).as_posix(),
        }
    else:
        silver_storage_path = {
            "dim_tempo": Path(
                BASE_DIR,
                base_path,
                "dim_tempo",
                "dim_tempo.parquet",
            ).as_posix(),
            "dim_condicao_metereologica": Path(
                BASE_DIR,
                base_path,
                "dim_condicao_metereologica",
                "dim_condicao_metereologica.parquet",
            ).as_posix(),
            "dim_pista": Path(
                BASE_DIR,
                base_path,
                "dim_pista",
                "dim_pista.parquet",
            ).as_posix(),
        }
    return silver_storage_path


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


def upsert(
    conn: duckdb.DuckDBPyConnection,
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script upsert.sql"""
    execute_query(
        conn=conn,
        query_key="upsert",
        query_dict=QUERIES,
        silver_storage_path=_set_silver_storage_path(settings=settings),
    )
