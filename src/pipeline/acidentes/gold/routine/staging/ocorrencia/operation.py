from functools import partial
from pathlib import Path
from typing import Callable, Optional, ContextManager

import duckdb
from prefect import task

from src.persistence.storage.settings import BucketSettings
from src.persistence.storage.utils import set_path
from src.persistence.database.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)

SILVER_STORAGE_PATH = Path(
    "acidentes",
    "silver",
    "fact",
    "ocorrencia",
).as_posix()
set_silver_storage_path = partial(
    set_path,
    base_path=SILVER_STORAGE_PATH,
)


@task(
    name="create_table",
    task_run_name="stg_ft_ocorrencia: create_table",
)
def create_table(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script create_table.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="create_table",
            query_dict=QUERIES,
            silver_storage_path=set_silver_storage_path(settings=settings),
        )


@task(
    name="process_routine",
    task_run_name="stg_ft_ocorrencia: process_routine",
)
def process_routine(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script create_table.sql"""
    create_future = create_table.submit(
        conn_fn=conn_fn,
        settings=settings,
    )
    create_future.result()
