from typing import Callable, Optional, ContextManager

import duckdb
from prefect import task

from src.persistence.storage.settings import BucketSettings
from src.persistence.database.operation import execute_query
from src.shared.system.file import load_module_queries
from .storage import (
    set_staging_storage_path,
    set_staging_log_path,
)

QUERIES = load_module_queries(current_file=__file__)


@task(
    name="fetch_partitions",
    task_run_name="fetch_partitions ['ano', 'uf']: ft_ocorrencia",
)
def fetch_partitions(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script fetch_partitions.sql"""
    with conn_fn() as conn:
        partitions_row = execute_query(
            conn=conn,
            query_key="fetch_partitions",
            query_dict=QUERIES,
            staging_log_path=set_staging_log_path(settings=settings),
        ).fetchall()

        anos, ufs = [], []
        for ano, uf in partitions_row:
            anos.append(ano)
            ufs.append(uf)

        return {
            "anos": anos,
            "ufs": ufs,
        }


@task(
    name="create_temp",
    task_run_name="create_temp: temp_ft_ocorrencia",
)
def create_temp(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script create_temp.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="create_temp",
            query_dict=QUERIES,
            staging_storage_path=set_staging_storage_path(settings=settings),
        )


@task(
    name="upsert_temp",
    task_run_name="upsert_temp: temp_ft_ocorrencia_{ano}_{uf}",
)
def upsert_temp(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    ano: int,
    uf: str,
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script upsert_temp.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="upsert_temp",
            query_dict=QUERIES,
            staging_storage_path=set_staging_storage_path(settings=settings),
            ano=ano,
            uf=uf,
        )


@task(
    name="upsert",
    task_run_name="upsert: ft_ocorrencia",
)
def upsert(conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]]):
    """Delega a execução do script upsert.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="upsert",
            query_dict=QUERIES,
        )
