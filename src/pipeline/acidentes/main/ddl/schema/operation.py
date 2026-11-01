from typing import Callable, ContextManager

import duckdb
from prefect import task

from src.persistence.database.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


@task(
    name="create",
    task_run_name="create: {schema_name}",
)
def create(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    schema_name: str,
    catalog_name: str,
):
    """Delega a execução do script create.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="create",
            query_dict=QUERIES,
            schema_name=schema_name,
            catalog_name=catalog_name,
        )
