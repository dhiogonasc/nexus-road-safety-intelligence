from typing import Callable, ContextManager

import duckdb
from prefect import task

from src.persistence.database.operation import execute
from .constants.sql import QUERIES_SQL


@task(
    name="create_schema",
    task_run_name="create_schema: {schema_name}",
)
def create_schema(
    schema_name: str,
    catalog_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
):
    """Delega a execução do script create_schema.sql"""
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=QUERIES_SQL["create_schema"],
            catalog_name=catalog_name,
            schema_name=schema_name,
        )
