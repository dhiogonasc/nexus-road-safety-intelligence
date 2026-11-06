from functools import partial
from typing import Callable, ContextManager, List, Optional

import duckdb
from prefect import flow, task, unmapped

from src.persistence.storage.settings import BucketSettings
from src.persistence.database.settings import settings_temp
from src.persistence.database.operation import (
    load_extensions,
    create_connection,
)
from src.pipeline.acidentes.temp.task.ingestion.bronze.operation import (
    stage_table,
    log_table_charge,
    copy_table_to_parquet,
)
from src.pipeline.acidentes.temp.task.ingestion.bronze.constants.summary import TABLES


@task(
    name="_bronze_ingestion_flow_factory",
    task_run_name="_bronze_ingestion_flow_factory: {table_name}",
)
def _ingestion_flow_factory(
    table_name: str,
    source_data: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    stage_future = stage_table.submit(
        table_name=table_name,
        source_data_path=source_data,
        conn_fn=conn_fn,
    )

    storage_futures = []
    log_future = log_table_charge.submit(
        table_name=table_name,
        conn_fn=conn_fn,
        settings=settings,
        wait_for=[stage_future],
    )
    storage_futures.append(log_future)

    copy_future = copy_table_to_parquet.submit(
        table_name=table_name,
        conn_fn=conn_fn,
        settings=settings,
        wait_for=[stage_future],
    )
    storage_futures.append(copy_future)

    for future in storage_futures:
        future.result()


@flow(
    name="bronze_ingestion_flow",
    flow_run_name="bronze_ingestion_flow",
)
def ingestion_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    table_name_list = [item["table_name"] for item in TABLES]
    source_data_list = [item["source_data_path"] for item in TABLES]

    futures = _ingestion_flow_factory.map(
        table_name=table_name_list,
        source_data=source_data_list,
        conn_fn=unmapped(conn_fn),
        settings=unmapped(settings),
    )

    for future in futures:
        future.result()


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
        database=settings_temp.database(
            name="acidentes",
            db_dir="acidentes",
        ),
    )

    ingestion_flow(conn_fn=conn_fn)
