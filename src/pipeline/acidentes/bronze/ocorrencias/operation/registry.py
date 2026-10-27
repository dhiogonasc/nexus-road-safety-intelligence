from pathlib import Path
from typing import Optional

import duckdb

from constants import BASE_DIR
from settings import BucketSettings
from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


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

    base_path = Path("acidentes", "bronze", "ocorrencias").as_posix()
    if settings:
        storage_path = Path(f"s3://{settings.STORAGE_BUCKET}", base_path).as_posix()
    else:
        storage_path = Path(BASE_DIR, base_path).as_posix()

    execute_query(
        conn=conn,
        query_key="copy",
        query_dict=QUERIES,
        storage_path=storage_path,
    )


def log(
    conn: duckdb.DuckDBPyConnection,
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script log.sql"""

    base_path = Path("acidentes", "bronze", "ocorrencias").as_posix()
    base_log_path = Path("acidentes", "bronze", "log", "ocorrencias").as_posix()

    if settings:
        storage_path = Path(f"s3://{settings.STORAGE_BUCKET}", base_path).as_posix()
        log_path = Path(f"s3://{settings.STORAGE_BUCKET}", base_log_path).as_posix()
    else:
        storage_path = Path(BASE_DIR, base_path).as_posix()
        log_path = Path(BASE_DIR, base_log_path).as_posix()

    execute_query(
        conn=conn,
        query_key="log",
        query_dict=QUERIES,
        storage_path=storage_path,
        log_path=log_path,
    )
