"""src/pipeline/bronze/extract.py"""

import duckdb

from config import BucketSettings
from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def copy_raw_to_parquet(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
    domain: str,
    table_name: str,
    csv_path: str,
    delim: str = ";",
    encoding: str = "latin-1",
) -> None:
    """Consolida a ingestão de dados csv em parquet"""
    execute_query(
        conn=conn,
        query_key="copy_raw_to_parquet",
        query_dict=QUERIES,
        settings=settings,
        domain=domain,
        table_name=table_name,
        csv_path=csv_path,
        delim=delim,
        encoding=encoding,
    )
