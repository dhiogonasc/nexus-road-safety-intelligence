"""src/pipeline/bronze/extract.py"""

import duckdb

from config import BucketSettings
from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def create_bronze_table_from_csv(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
    domain: str,
    table: str,
    csv_path: str,
    delim: str = ";",
    encoding: str = "latin-1",
) -> None:
    """Consolida a ingestão de dados csv em stage"""
    execute_query(
        conn=conn,
        query_key="create_bronze_table_from_csv",
        query_dict=QUERIES,
        settings=settings,
        domain=domain,
        table=table,
        csv_path=csv_path,
        delim=delim,
        encoding=encoding,
    )
