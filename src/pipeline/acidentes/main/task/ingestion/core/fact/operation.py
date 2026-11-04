from typing import Callable, ContextManager, Optional

import duckdb
from prefect import task

from src.persistence.storage.utils import get_storage_path
from src.persistence.storage.settings import BucketSettings
from src.persistence.database.operation import execute
from .constants.sql import QUERIES_SQL
from .constants.storage import BASE_PATH
from .shared.operation import fetch_table_partitions


@task(
    name="_upsert_partition",
    task_run_name="_upsert_partition: {filter_clause}",
)
def _upsert_partition(
    table_name: str,
    catalog_name: str,
    filter_clause: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=QUERIES_SQL[table_name],
            catalog_name=catalog_name,
            filter_clause=filter_clause,
            storage_path=get_storage_path(
                table_name=table_name,
                base_path=BASE_PATH,
                settings=settings,
            ),
        )


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
    partitions = fetch_table_partitions.submit(
        source_table=table_name,
        source_base_path=BASE_PATH,
        conn_fn=conn_fn,
        settings=settings,
    ).result()

    filter_clauses = [
        " ".join(
            f"AND {k} = {f"'{v}'" if isinstance(v, str) else v}"
            for k, v in partition.items()
        )
        for partition in partitions
    ]

    for filter_clause in filter_clauses:
        _upsert_partition(
            table_name=table_name,
            catalog_name=catalog_name,
            filter_clause=filter_clause,
            conn_fn=conn_fn,
            settings=settings,
        )
