from pathlib import Path
from typing import Callable, ContextManager, Optional

import duckdb
from prefect import task

from src.persistence.storage.settings import BucketSettings
from src.persistence.database.operation import execute_query
from src.shared.system.file import load_module_queries
from .storage import (
    set_storage_path,
    set_dim_storage_path,
)

QUERIES = load_module_queries(current_file=__file__)


@task(
    name="bootstrap",
    task_run_name="bootstrap: agg_letalidade_pista_clima",
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
    name="copy_to_parquet",
    task_run_name="copy_to_parquet: agg_letalidade_pista_clima",
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
    name="create",
    task_run_name="create: agg_letalidade_pista_clima",
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
    name="upsert",
    task_run_name="upsert: agg_letalidade_pista_clima",
)
def upsert(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script upsert.sql"""
    dim_storage_path = {
        "dim_local_storage_path": Path(
            set_dim_storage_path(settings=settings),
            "local",
        ).as_posix(),
        "dim_pista_storage_path": Path(
            set_dim_storage_path(settings=settings),
            "pista",
        ).as_posix(),
        "dim_clima_storage_path": Path(
            set_dim_storage_path(settings=settings),
            "clima",
        ).as_posix(),
        "dim_categoria_storage_path": Path(
            set_dim_storage_path(settings=settings),
            "categoria",
        ).as_posix(),
    }

    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="upsert",
            query_dict=QUERIES,
            **dim_storage_path,
        )
