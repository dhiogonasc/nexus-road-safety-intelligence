from pathlib import Path
from typing import Optional

import duckdb

from constants import BASE_DIR
from settings import BucketSettings
from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def stage_ft_ocorrencias(
    conn: duckdb.DuckDBPyConnection,
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script stage_ft_ocorrencias.sql"""
    
    silver_ft_base_path = Path("acidentes", "silver", "fato", "ocorrencias").as_posix()

    if settings:
        silver_ft_storage_path = Path(f"s3://{settings.STORAGE_BUCKET}", silver_ft_base_path).as_posix()
    else:
        silver_ft_storage_path = Path(BASE_DIR, silver_ft_base_path).as_posix()

    execute_query(
        conn=conn,
        query_key="stage",
        query_dict=QUERIES,
        storage_path=silver_ft_storage_path,
    )