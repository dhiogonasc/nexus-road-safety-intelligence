from typing import Callable, ContextManager, Optional

import duckdb
from prefect import task

from src.persistence.storage.utils import (
    get_log_path,
    get_storage_path,
)
from src.persistence.database.operation import execute
from src.persistence.storage.settings import BucketSettings
from .constants.sql import (
    CREATE_QUERIES_SQL,
    BOOTSTRAP_QUERIES_SQL,
    LOG_CHARGE_QUERIES_SQL,
    COPY_TO_PARQUET_QUERIES_SQL,
    UPSERT_BY_PARTITIONS_QUERIES_SQL,
)
from .constants.storage import BASE_PATH
from ..staging.constants.storage import BASE_PATH as SOURCE_BASE_PATH
from .shared.operation import fetch_table_partitions


@task(
    name="create_table",
    task_run_name="create_table: {table_name}",
)
def create_table(
    table_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
):
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=CREATE_QUERIES_SQL[table_name],
        )


@task(
    name="bootstrap_table",
    task_run_name="bootstrap_table: {table_name}",
)
def bootstrap_table(
    table_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    with conn_fn() as conn:
        try:
            execute(
                conn=conn,
                query=BOOTSTRAP_QUERIES_SQL[table_name],
                storage_path=get_storage_path(
                    table_name=table_name,
                    base_path=BASE_PATH,
                    settings=settings,
                ),
            )
        except duckdb.IOException:
            pass


@task(
    name="copy_table_to_parquet",
    task_run_name="copy_table_to_parquet: {table_name}",
)
def copy_table_to_parquet(
    table_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=COPY_TO_PARQUET_QUERIES_SQL[table_name],
            storage_path=get_storage_path(
                table_name=table_name,
                base_path=BASE_PATH,
                settings=settings,
            ),
        )


@task(
    name="log_table_charge",
    task_run_name="log_table_charge: {table_name}",
)
def log_table_charge(
    table_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=LOG_CHARGE_QUERIES_SQL[table_name],
            log_path=get_log_path(
                table_name=table_name,
                base_path=BASE_PATH,
                settings=settings,
            ),
        )


@task(
    name="upsert_table_by_partitions",
    task_run_name="upsert_table_by_partitions: {table_name}",
)
def upsert_table_by_partitions(
    table_name: str,
    source_table: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    fetch_partitions_future = fetch_table_partitions.submit(
        source_table=source_table,
        source_base_path=SOURCE_BASE_PATH,
        conn_fn=conn_fn,
        settings=settings,
    )
    partitions = fetch_partitions_future.result()

    for partition in partitions:
        filter_clauses_list = []
        for key, val in partition.items():
            formatted_val = f"'{val}'" if isinstance(val, str) else str(val)
            filter_clauses_list.append(f"AND {key} = {formatted_val}\n")

    filter_clause = "\n ".join(filter_clauses_list)

    with conn_fn() as conn:
        execute(
            conn=conn,
            query=UPSERT_BY_PARTITIONS_QUERIES_SQL[table_name],
            filter_clause=filter_clause,
            source_storage_path=get_storage_path(
                table_name=source_table,
                base_path=SOURCE_BASE_PATH,
                settings=settings,
            ),
        )
