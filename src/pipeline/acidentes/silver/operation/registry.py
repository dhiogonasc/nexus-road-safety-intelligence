from shared.db.operation import execute_query

import duckdb

from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def create(conn: duckdb.DuckDBPyConnection):
    execute_query(
        conn=conn,
        query_key="create",
        query_dict=QUERIES,
    )
