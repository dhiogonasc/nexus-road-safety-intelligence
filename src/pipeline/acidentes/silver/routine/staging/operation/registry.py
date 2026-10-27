from pathlib import Path
from typing import Optional

import duckdb

from constants import BASE_DIR
from settings import BucketSettings
from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def fetch(
    conn: duckdb.DuckDBPyConnection,
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script fetch.sql"""

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
        query_key="fetch",
        query_dict=QUERIES,
        storage_path=storage_path,
        log_path=log_path,
    )