from functools import partial
from pathlib import Path
from typing import Callable, List, Optional, ContextManager

import duckdb
from prefect import task
from prefect.futures import PrefectFuture

from src.persistence.storage.settings import BucketSettings
from src.persistence.storage.utils import set_path
from src.persistence.database.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)

STG_STORAGE_PATH = Path(
    "acidentes",
    "silver",
    "staging",
    "ocorrencia",
).as_posix()
set_staging_storage_path = partial(
    set_path,
    base_path=STG_STORAGE_PATH,
)

STG_LOG_PATH = Path(
    "acidentes",
    "silver",
    "staging",
    "log",
    "ocorrencia",
).as_posix()
set_staging_log_path = partial(
    set_path,
    base_path=STG_LOG_PATH,
)


@task(
    name="fetch_partitions",
    task_run_name="ft_ocorrencia: fetch_partitions ['ano', 'uf']",
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
    name="create_temp_stg_table",
    task_run_name="temp_ft_ocorrencia: create_temp_stg_table",
)
def create_temp_stg_table(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="create_temp_stg_table",
            query_dict=QUERIES,
            staging_storage_path=set_staging_storage_path(settings=settings),
        )


@task(
    name="upsert_temp_stg_table",
    task_run_name="temp_ft_ocorrencia_{ano}_{uf}: upsert_temp_stg_table",
)
def upsert_temp_stg_table(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    ano: int,
    uf: str,
    settings: Optional[BucketSettings] = None,
):
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="upsert_temp_stg_table",
            query_dict=QUERIES,
            staging_storage_path=set_staging_storage_path(settings=settings),
            ano=ano,
            uf=uf,
        )


@task(
    name="upsert_table",
    task_run_name="ft_ocorrencia: upsert_table",
)
def upsert_table(conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]]):
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="upsert_table",
            query_dict=QUERIES,
        )


@task(
    name="process_partitions",
    task_run_name="ft_ocorrencia: process_partitions",
)
def process_partitions(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    upstream_tasks: List[PrefectFuture],
    settings: Optional[BucketSettings] = None,
):
    create_temp_future = create_temp_stg_table.submit(
        conn_fn=conn_fn,
        wait_for=upstream_tasks,
    )

    fetch_partitions_future = fetch_partitions.submit(
        conn_fn=conn_fn,
        settings=settings,
    )

    partitions_data = fetch_partitions_future.result()

    upsert_temp_futures = upsert_temp_stg_table.map(
        conn_fn=conn_fn,
        ano=partitions_data["anos"],
        uf=partitions_data["ufs"],
        settings=settings,
        wait_for=[create_temp_future],
    )

    upsert_future = upsert_table.submit(
        conn_fn=conn_fn,
        wait_for=upsert_temp_futures,
    )
    upsert_future.result()
