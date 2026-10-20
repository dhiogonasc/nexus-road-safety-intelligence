"""src/pipeline/setup/extension.py"""

import duckdb

from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def install_extension(
    conn: duckdb.DuckDBPyConnection,
    extension: str,
) -> None:
    """Delega a execucao do script install_extension.sql"""
    execute_query(
        conn=conn,
        query_key="install_extension",
        query_dict=QUERIES,
        extension=extension,
    )


def create_bucket_secret(
    conn: duckdb.DuckDBPyConnection,
    storage_access_key_id: str,
    storage_secret_access_key: str,
    storage_region: str,
    storage_endpoint: str,
) -> None:
    """Delega a execucao do script create_bucket_secret.sql"""
    execute_query(
        conn=conn,
        query_key="create_bucket_secret",
        query_dict=QUERIES,
        storage_access_key_id=storage_access_key_id,
        storage_secret_access_key=storage_secret_access_key,
        storage_region=storage_region,
        storage_endpoint=storage_endpoint,
    )
