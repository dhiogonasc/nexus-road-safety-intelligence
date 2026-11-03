from functools import partial
from typing import Callable, ContextManager, List, Optional

import duckdb
from prefect import flow, task

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


@flow(
    name="bronze_ingestion_flow",
    flow_run_name="bronze_ingestion_flow",
)
def ingestion_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    table_names = [item["table_name"] for item in TABLES]
    source_data_paths = [item["source_data_path"] for item in TABLES]

    storage_futures = []
    stage_futures = stage_table.map(
        table_name=table_names,
        source_data_path=source_data_paths,
        conn_fn=conn_fn,
    )
    log_futures = log_table_charge.map(
        table_name=table_names,
        conn_fn=conn_fn,
        settings=settings,
        wait_for=[stage_futures],
    )
    storage_futures.append(log_futures)

    copy_futures = copy_table_to_parquet.map(
        table_name=table_names,
        conn_fn=conn_fn,
        settings=settings,
        wait_for=[stage_futures],
    )
    storage_futures.append(copy_futures)

    for future in storage_futures:
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
