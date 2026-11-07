from typing import Callable, ContextManager, Optional

import duckdb
from prefect import task

from src.persistence.storage.utils import get_log_path
from persistence.database.provider import execute
from src.persistence.storage.settings import BucketSettings
from .constants.sql import SHARED_QUERIES_SQL


@task(
    name="fetch_table_partitions",
    task_run_name="fetch_table_partitions: {source_table}",
)
def fetch_table_partitions(
    source_table: str,
    source_base_path: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    with conn_fn() as conn:
        result = execute(
            conn=conn,
            query=SHARED_QUERIES_SQL["fetch_partitions"],
            source_log_path=get_log_path(
                table_name=source_table,
                base_path=source_base_path,
                settings=settings,
            ),
        )

        keys = [desc[0] for desc in result.description]
        values = dict.fromkeys(result.fetchall()).keys()
    
    return [dict(zip(keys, values_row)) for values_row in values]
