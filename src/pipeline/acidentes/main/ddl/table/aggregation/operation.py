from typing import Callable, ContextManager

import duckdb
from prefect import task

from src.shared.system.file import load_module_queries
from src.persistence.database.operation import execute_query

QUERIES = load_module_queries(current_file=__file__)
AGG_TABLES = list(QUERIES.keys())

@task(
    name="create",
    task_run_name="create: {table_name}",
)
def create(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    table_name: str,
    catalog_name: str,
):
    """Delega a execução do script create.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key=table_name,
            query_dict=QUERIES,
            catalog_name=catalog_name,
        )