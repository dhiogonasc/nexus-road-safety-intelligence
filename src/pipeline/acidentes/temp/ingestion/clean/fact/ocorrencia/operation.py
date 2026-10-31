from typing import Callable, List, Optional, ContextManager

import duckdb
from prefect import task
from prefect.futures import PrefectFuture

from src.persistence.storage.settings import BucketSettings
from src.persistence.database.operation import execute_query
from src.shared.system.file import load_module_queries
from .partition.operation import (
    create_temp,
    fetch_partitions,
    upsert_temp,
    upsert,
)
from .storage import set_storage_path

QUERIES = load_module_queries(current_file=__file__)


@task(
    name="create",
    task_run_name="create: ft_ocorrencia",
)
def create(conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]]):
    """Delega a execução do script create.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="create",
            query_dict=QUERIES,
        )


@task(
    name="bootstrap",
    task_run_name="bootstrap: ft_ocorrencia",
)
def bootstrap(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script bootstrap.sql"""
    with conn_fn() as conn:
        try:
            execute_query(
                conn=conn,
                query_key="bootstrap",
                query_dict=QUERIES,
                storage_path=set_storage_path(settings=settings),
            )
        except duckdb.IOException:
            pass


@task(
    name="upsert_by_partitions",
    task_run_name="upsert_by_partitions: ft_ocorrencia",
)
def upsert_by_partitions(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    create_temp_future = create_temp.submit(conn_fn=conn_fn)

    fetch_partitions_future = fetch_partitions.submit(
        conn_fn=conn_fn,
        settings=settings,
    )

    partitions_data = fetch_partitions_future.result()

    upsert_temp_futures = upsert_temp.map(
        conn_fn=conn_fn,
        ano=partitions_data["anos"],
        uf=partitions_data["ufs"],
        settings=settings,
        wait_for=[create_temp_future],
    )

    upsert_future = upsert.submit(
        conn_fn=conn_fn,
        wait_for=upsert_temp_futures,
    )
    upsert_future.result()


@task(
    name="copy_to_parquet",
    task_run_name="copy_to_parquet: ft_ocorrencia",
)
def copy_to_parquet(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script copy_to_parquet.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="copy_to_parquet",
            query_dict=QUERIES,
            storage_path=set_storage_path(settings=settings),
        )
