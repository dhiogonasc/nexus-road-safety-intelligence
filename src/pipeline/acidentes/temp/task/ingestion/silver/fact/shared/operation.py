from typing import Callable, ContextManager, Optional

import duckdb
from prefect import task

from ...staging.utils.storage import set_log_path
from src.persistence.database.operation import execute
from src.persistence.storage.settings import BucketSettings

from .constants.sql import SHARED_QUERIES_SQL


@task(
    name="fetch_partitions",
    task_run_name="fetch_partitions: {stg_table_name}",
)
def fetch_partitions(
    stg_table_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script de fetch_partitions"""
    with conn_fn() as conn:
        result = execute(
            conn=conn,
            query=SHARED_QUERIES_SQL["fetch_partitions"],
            staging_log_path=set_log_path(
                table_name=stg_table_name,
                settings=settings,
            ),
        )

        rows = result.fetchall()

        if not rows:
            return {}

        partition_keys = [desc[0] for desc in result.description]
        partition_values = dict.fromkeys(rows).keys()

        return [
            dict(zip(partition_keys, values_row)) for values_row in partition_values
        ]
