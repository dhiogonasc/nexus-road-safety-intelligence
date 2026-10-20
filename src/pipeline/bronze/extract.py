"""src/pipeline/bronze/extract.py"""

import duckdb

from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def create_bucket_secret(
    conn: duckdb.DuckDBPyConnection,
    secret_name: str,
    storage_access_key_id: str,
    storage_secret_access_key: str,
    storage_region: str,
    storage_endpoint: str,
) -> None:
    """Consolida o registro do secret para a sessao"""
    execute_query(
        conn=conn,
        query_key="create_bucket_secret",
        query_dict=QUERIES,
        secret_name=secret_name,
        storage_access_key_id=storage_access_key_id,
        storage_secret_access_key=storage_secret_access_key,
        storage_region=storage_region,
        storage_endpoint=storage_endpoint,
    )


def create_bronze_table_from_csv(
    conn: duckdb.DuckDBPyConnection,
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
        table=table,
        csv_path=csv_path,
        delim=delim,
        encoding=encoding,
    )


def copy_bronze_table_to_parquet(
    conn: duckdb.DuckDBPyConnection,
    bucket_name: str,
    domain: str,
    table: str,
) -> None:
    """Consolida o registro bronze em bucket parquet"""
    execute_query(
        conn=conn,
        query_key="copy_bronze_table_to_parquet",
        query_dict=QUERIES,
        domain=domain,
        table=table,
        bucket_name=bucket_name,
    )
