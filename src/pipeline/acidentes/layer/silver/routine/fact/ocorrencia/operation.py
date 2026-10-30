from functools import partial
from pathlib import Path
from typing import Callable, Optional, ContextManager

import duckdb
from prefect import task

from src.persistence.storage import BucketSettings
from src.persistence.storage.utils import set_path
from src.persistence.database.operation import execute_query
from src.shared.system.file import load_module_queries
from .partitions.operation import process_partitions

QUERIES = load_module_queries(current_file=__file__)

STORAGE_PATH = Path(
    "acidentes",
    "silver",
    "ft_ocorrencia",
).as_posix()
set_storage_path = partial(
    set_path,
    base_path=STORAGE_PATH,
)


@task(
    name="create_table",
    task_run_name="ft_ocorrencia: create_table",
)
def create_table(conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]]):
    """Delega a execução do script create_table.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="create_table",
            query_dict=QUERIES,
        )


@task(
    name="bootstrap_table",
    task_run_name="ft_ocorrencia: bootstrap_table",
)
def bootstrap_table(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script bootstrap_table.sql"""
    with conn_fn() as conn:
        try:
            execute_query(
                conn=conn,
                query_key="bootstrap_table",
                query_dict=QUERIES,
                storage_path=set_storage_path(settings=settings),
            )
        except duckdb.IOException:
            pass


@task(
    name="copy_to_parquet",
    task_run_name="ft_ocorrencia: copy_to_parquet",
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


@task(
    name="process_routine",
    task_run_name="ft_ocorrencia: process_routine",
)
def process_routine(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    create_future = create_table.submit(conn_fn=conn_fn)

    bootstrap_future = bootstrap_table.submit(
        conn_fn=conn_fn,
        settings=settings,
        wait_for=[create_future],
    )

    process_partitions_future = process_partitions.submit(
        conn_fn=conn_fn,
        settings=settings,
        upstream_tasks=[bootstrap_future],
    )

    copy_future = copy_to_parquet.submit(
        conn_fn=conn_fn,
        settings=settings,
        wait_for=[process_partitions_future],
    )
    copy_future.result()
