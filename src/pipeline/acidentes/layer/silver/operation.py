from typing import Callable, Optional, ContextManager

import duckdb
from prefect import flow, task

from src.shared.system.file import load_module_queries
from src.persistence.storage.settings import BucketSettings
from src.persistence.database.operation import execute_query
from .routine import routines

QUERIES = load_module_queries(current_file=__file__)


@task(
    name="Create Layer Schema",
    task_run_name="create bronze schema",
)
def create_schema(conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]]):
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="create_schema",
            query_dict=QUERIES,
        )


@flow(
    name="Process Layer",
    flow_run_name="process silver",
)
def process_layer(
    conn_fn: Callable,
    settings: Optional[BucketSettings] = None,
):
    create_future = create_schema.submit(conn_fn=conn_fn)

    routine_futures = {}
    for routine in routines:

        wait_for = [create_future]
        for dep_routine in routine["depends_on"]:
            label = dep_routine["label"]
            if label in routine_futures:
                wait_for.append(routine_futures[label])

        routine_future = routine["processor"].submit(
            conn_fn=conn_fn,
            settings=settings,
            wait_for=wait_for,
        )

        routine_futures[routine["label"]] = routine_future

    for routine_future in routine_futures.values():
        routine_future.result()
