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
