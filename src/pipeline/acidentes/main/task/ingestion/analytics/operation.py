from typing import Callable, ContextManager, Optional

import duckdb
from prefect import task

from src.persistence.storage.utils import get_storage_path
from src.persistence.storage.settings import BucketSettings
from persistence.database.provider import execute
from .constants.sql import QUERIES_SQL
from .constants.storage import BASE_PATH


@task(
    name="upsert_table",
    task_run_name="upsert_table: {table_name}",
)
def upsert_table(
    table_name: str,
    catalog_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=QUERIES_SQL[table_name],
            catalog_name=catalog_name,
            storage_path=get_storage_path(
                table_name=table_name,
                base_path=BASE_PATH,
                settings=settings,
            ),
        )
