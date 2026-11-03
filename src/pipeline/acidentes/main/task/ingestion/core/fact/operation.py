from typing import Callable, ContextManager, Optional

import duckdb
from prefect import task

from src.persistence.storage.settings import BucketSettings
from src.persistence.database.operation import execute
from .utils.storage import get_table_source_path
from .constants.sql import QUERIES_SQL


@task(
    name="upsert_table",
    task_run_name="upsert_table: {table_name}",
)
def upsert_table(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    table_name: str,
    catalog_name: str,
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script de upsert"""
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=QUERIES_SQL[table_name],
            catalog_name=catalog_name,
            source_storage_path=get_table_source_path(
                table_name=table_name,
                settings=settings,
            ),
        )
