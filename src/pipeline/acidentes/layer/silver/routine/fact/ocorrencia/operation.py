from collections import defaultdict
from functools import partial
from pathlib import Path
from typing import Callable, List, Optional, ContextManager

import duckdb
from prefect import task
from prefect.futures import PrefectFuture

from src.persistence.storage import BucketSettings
from src.persistence.storage.utils import set_path
from src.persistence.database.operation import execute_query
from src.shared.system.file import load_module_queries

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

STG_STORAGE_PATH = Path(
    "acidentes",
    "silver",
    "stg",
).as_posix()
set_staging_storage_path = partial(
    set_path,
    base_path=STG_STORAGE_PATH,
)

STG_LOG_PATH = Path(
    "acidentes",
    "silver",
    "log",
    "stg",
).as_posix()
set_staging_log_path = partial(
    set_path,
    base_path=STG_LOG_PATH,
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
    name="fetch_partitions",
    task_run_name="ft_ocorrencia: fetch_partitions ['ano', 'uf']",
)
def fetch_partitions(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script fetch_partitions.sql"""
    with conn_fn() as conn:
        partitons_row = execute_query(
            conn=conn,
            query_key="fetch_partitions",
            query_dict=QUERIES,
            staging_log_path=set_staging_log_path(settings=settings),
        ).fetchall()

    partition_agg = defaultdict(list)
    for ano, uf in partitons_row:
        partition_agg[ano].append(uf)

    return [{ano: ufs} for ano, ufs in partition_agg.items()]


@task(
    name="create_temp_stg_table",
    task_run_name="temp_ft_ocorrencia_{ano}_{uf}: create_temp_stg_table",
)
def create_temp_stg_table(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    ano: int,
    uf: str,
    settings: Optional[BucketSettings] = None,
):
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="create_temp_stg_table",
            query_dict=QUERIES,
            staging_storage_path=set_staging_storage_path(settings=settings),
            ano=ano,
            uf=uf,
        )


@task(
    name="upsert_table",
    task_run_name="ft_ocorrencia: upsert_table - {ano}: {uf}",
)
def upsert_table(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    ano: int,
    uf: str,
):
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="upsert_table",
            query_dict=QUERIES,
            ano=ano,
            uf=uf,
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
    create_temp_futures = []
    for partition in fetch_partitions(
        conn_fn=conn_fn,
        settings=settings,
    ):
        for ano, ufs in partition.items():
            for uf in ufs:
                create_temp_future = create_temp_stg_table.submit(
                    conn_fn=conn_fn,
                    ano=ano,
                    uf=uf,
                    settings=settings,
                    wait_for=upstream_tasks,
                )
                create_temp_futures.append(create_temp_future)

        for ano, ufs in partition.items():
            for uf in ufs:
                upsert_future = upsert_table.submit(
                    conn_fn=conn_fn,
                    ano=ano,
                    uf=uf,
                    wait_for=[create_temp_futures],
                )
                upsert_future.result()


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
