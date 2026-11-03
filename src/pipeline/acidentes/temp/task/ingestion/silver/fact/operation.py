from typing import Callable, ContextManager, Optional

import duckdb
from prefect import task

from src.persistence.database.operation import execute
from src.persistence.storage.settings import BucketSettings
from .utils.storage import set_storage_path
from .constants.sql import (
    CREATE_QUERIES_SQL,
    BOOTSTRAP_QUERIES_SQL,
    COPY_TO_PARQUET_QUERIES_SQL,
)
from .shared.operation import fetch_partitions
from .partitions.operation import (
    create_temp_table,
    upsert_temp_table,
    upsert_ft_table,
)


@task(
    name="create_table",
    task_run_name="create_table: {table_name}",
)
def create_table(
    table_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
):
    """Delega a execução do script de create"""
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
    """Delega a execução do script de bootstrap"""
    with conn_fn() as conn:
        try:
            execute(
                conn=conn,
                query=BOOTSTRAP_QUERIES_SQL[table_name],
                storage_path=set_storage_path(
                    table_name=table_name,
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
    """Delega a execução do script de copy_to_parquet"""
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=COPY_TO_PARQUET_QUERIES_SQL[table_name],
            storage_path=set_storage_path(
                table_name=table_name,
                settings=settings,
            ),
        )


@task(
    name="upsert_table_by_partitions",
    task_run_name="upsert_table_by_partitions: {target_table}",
)
def upsert_table_by_partitions(
    target_table: str,
    source_table: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    create_temp_future = create_temp_table.submit(
        target_table=target_table,
        conn_fn=conn_fn,
    )

    fetch_partitions_future = fetch_partitions.submit(
        stg_table_name=source_table,
        conn_fn=conn_fn,
        settings=settings,
    )

    partitions = fetch_partitions_future.result()

    if not partitions:
        return

    upsert_temp_futures = []
    for partition in partitions:
        partition_values = "_".join([str(val) for val in partition.values()])

        filter_clauses_list = []
        for key, val in partition.items():
            formatted_val = f"'{val}'" if isinstance(val, str) else str(val)
            filter_clauses_list.append(f"AND {key} = {formatted_val}\n")

        filter_clause = "\n ".join(filter_clauses_list)

        future = upsert_temp_table.submit(
            target_table=target_table,
            source_table=source_table,
            partition_values=partition_values,
            filter_clause=filter_clause,
            conn_fn=conn_fn,
            wait_for=[
                create_temp_future,
                fetch_partitions_future,
            ],
        )
        upsert_temp_futures.append(future)

    upsert_future = upsert_ft_table.submit(
        target_table=target_table,
        conn_fn=conn_fn,
        wait_for=upsert_temp_futures,
    )

    upsert_future.result()
