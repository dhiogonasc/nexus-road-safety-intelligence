from functools import partial
from typing import Callable, ContextManager, Optional

import duckdb
from prefect import flow

from src.persistence.database.settings import settings_temp
from src.persistence.database.operation import create_connection, load_extensions
from src.persistence.storage.settings import BucketSettings
from ...task.ingestion.raw import raw_tasks


@flow(
    name="raw_ingestion_flow",
    flow_run_name="raw_ingestion_flow",
)
def raw_ingestion_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    futures = [
        task.submit(
            conn_fn=conn_fn,
            settings=settings,
        )
        for task in raw_tasks
    ]
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
        database=settings_temp.database(name="acidentes"),
    )

    raw_ingestion_flow(conn_fn=conn_fn)
