from functools import partial
from pathlib import Path
from typing import Optional, Callable, ContextManager

import duckdb
from prefect import task

from src.persistence.storage.settings import BucketSettings
from src.persistence.storage.utils import set_path
from src.persistence.database.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)

STORAGE_PATH = Path(
    "acidentes",
    "gold",
    "aggregation",
    "dispersao_geo_temporal",
).as_posix()
set_storage_path = partial(
    set_path,
    base_path=STORAGE_PATH,
)

DIM_STORAGE_BASE_PATH = Path(
    "acidentes",
    "silver",
    "dimension",
).as_posix()
set_dim_storage_path = partial(
    set_path,
    base_path=DIM_STORAGE_BASE_PATH,
)


@task(
    name="Bootstrap Table",
    task_run_name="agg_dispersao_geo_temporal: bootstrap_table",
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
    name="Copy Table to Parquet",
    task_run_name="agg_dispersao_geo_temporal: copy_to_parquet",
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
    name="Create Table",
    task_run_name="agg_dispersao_geo_temporal: create_table",
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
    name="Upsert Table",
    task_run_name="agg_dispersao_geo_temporal: upsert_table",
)
def upsert_table(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script upsert_table.sql"""
    dim_storage_path = {
        "dim_local_storage_path": Path(
            set_dim_storage_path(settings=settings),
            "local",
        ).as_posix(),
        "dim_tempo_storage_path": Path(
            set_dim_storage_path(settings=settings),
            "tempo",
        ).as_posix(),
    }

    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="upsert_table",
            query_dict=QUERIES,
            **dim_storage_path,
        )


@task(
    name="process_routine",
    task_run_name="agg_dipsersao_geo_temporal: process_routine",
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

    upsert_future = upsert_table.submit(
        conn_fn=conn_fn,
        wait_for=[bootstrap_future],
    )

    copy_future = copy_to_parquet.submit(
        conn_fn=conn_fn,
        settings=settings,
        wait_for=[upsert_future],
    )
    copy_future.result()
