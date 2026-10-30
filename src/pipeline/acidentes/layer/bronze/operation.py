from typing import Callable, Optional

import duckdb
from prefect import flow, task

from src.shared.system.file import load_module_queries
from src.persistence.storage.settings import BucketSettings
from src.persistence.database.operation import execute_query
from .routine import processors

QUERIES = load_module_queries(current_file=__file__)

required_extensions = [
    "httpfs",
    "parquet",
]


@task(
    name="Create Layer Schema",
    task_run_name="bronze: create schema",
)
def create_schema(conn_fn: Callable):
    with conn_fn() as conn:
        execute_query(
            conn=conn,
            query_key="create_schema",
            query_dict=QUERIES,
        )


@flow(
    name="Process Layer",
    flow_run_name="bronze: process layer",
)
def process_layer(
    conn_fn: Callable,
    settings: Optional[BucketSettings] = None,
):
    create_future = create_schema.submit(conn_fn=conn_fn)

    for processor in processors:
        futures = []
        future = processor.submit(
            conn_fn=conn_fn,
            settings=settings,
            wait_for=[create_future],
        )
        futures.append(future)

    for future in futures:
        future.result()
