from typing import Callable, ContextManager, Optional

import duckdb
from prefect import task

from src.persistence.storage.settings import BucketSettings
from src.shared.system.file import load_module_queries
from src.persistence.database.operation import execute_query
from .storage import set_storage_path_fn

QUERIES = load_module_queries(current_file=__file__)
FT_TABLES = list(QUERIES.keys())


@task(
    name="upsert",
    task_run_name="upsert: {table_name}",
)
def upsert(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    table_name: str,
    catalog_name: str,
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script upsert.sql"""
    set_storage_path = set_storage_path_fn(table_name=table_name)
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key=table_name,
            query_dict=QUERIES,
            catalog_name=catalog_name,
            storage_path=set_storage_path(settings=settings),
        )
