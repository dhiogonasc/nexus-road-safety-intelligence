from typing import Callable, Optional, ContextManager

import duckdb
from prefect import task

from src.persistence.storage.settings import BucketSettings
from src.persistence.database.operation import execute_query
from src.shared.system.file import load_module_queries
from .storage import set_silver_storage_path

QUERIES = load_module_queries(current_file=__file__)


@task(
    name="stage",
    task_run_name="stage: stg_ft_ocorrencia",
)
def stage(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script stage.sql"""
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="stage",
            query_dict=QUERIES,
            silver_storage_path=set_silver_storage_path(settings=settings),
        )
