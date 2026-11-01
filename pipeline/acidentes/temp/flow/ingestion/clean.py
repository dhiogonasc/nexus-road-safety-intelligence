from functools import partial
from typing import Callable, ContextManager, Optional, Sequence

import duckdb
from prefect import Task, flow

from src.persistence.database.settings import settings_temp
from src.persistence.database.operation import create_connection, load_extensions
from src.persistence.storage.settings import BucketSettings
from ...task.ingestion.clean import  clean_tasks


@flow(
    name="staging_clean_ingestion_flow",
    flow_run_name="staging_clean_ingestion_flow",
)
def clean_ingestion_flow_factory(
    tasks: Sequence[Task],
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    futures = [
        task.submit(
            conn_fn=conn_fn,
            settings=settings,
        )
        for task in tasks
    ]
    for future in futures:
        future.result()


@flow(
    name="clean_ingestion_flow",
    flow_run_name="clean_ingestion_flow",
)
def clean_ingestion_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):

    for clean_task_group in clean_tasks:
        clean_ingestion_flow_factory(
            tasks=clean_task_group,
            conn_fn=conn_fn,
            settings=settings,
        )


if __name__ == "__main__":
    load_extensions_fn = partial(
        load_extensions,
        extensions=[
            "httpfs",
            "parquet",
        ],
    )
    conn_fn = partial(
        create_connection,
        load_extensions_fn=load_extensions_fn,
        database=settings_temp.database(name="acidentes"),
    )

    clean_ingestion_flow(conn_fn=conn_fn)
