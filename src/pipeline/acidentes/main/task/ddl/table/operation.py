from typing import Callable, ContextManager

from beartype.typing import Dict
import duckdb
from prefect import task

from persistence.database.provider import execute
from .constants.sql import QUERIES_SQL


@task(
    name="create_table",
    task_run_name="create_table: {table_name}",
)
def create_table(
    table_name: str,
    catalog_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
):
    """Delega a execução do script QUERIES_SQL[table_name].sql"""
    with conn_fn() as conn:
        execute(
            conn=conn,
            catalog_name=catalog_name,
            query=QUERIES_SQL[table_name],
        )
