from typing import Callable, ContextManager

import duckdb
from prefect import task

from src.shared.system.file import load_module_queries
from src.persistence.database.operation import execute_query

QUERIES = load_module_queries(current_file=__file__)
AGG_TABLES = list(QUERIES.keys())

@task(
    name="create_table",
    task_run_name="create_table: {table_name}",
)
def create_table(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    table_name: str,
):
    """Delega a execução do script ddl.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key=table_name,
            query_dict=QUERIES,
        )