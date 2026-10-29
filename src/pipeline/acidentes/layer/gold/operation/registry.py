import duckdb

from src.persistence.database.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def create_schema(conn: duckdb.DuckDBPyConnection):
    execute_query(
        conn=conn,
        query_key="create_schema",
        query_dict=QUERIES,
    )
