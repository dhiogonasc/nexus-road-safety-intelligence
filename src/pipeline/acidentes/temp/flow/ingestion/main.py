from functools import partial
from typing import Callable, ContextManager, Optional

import duckdb
from prefect import flow

from src.persistence.storage.settings import BucketSettings
from src.persistence.database.settings import settings_temp
from persistence.database.provider import (
    load_extensions,
    create_connection,
)

from .layer import (
    bronze,
    silver,
    gold,
)


@flow(
    name="ingestion_flow",
    flow_run_name="ingestion_flow",
)
def ingestion_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    bronze.ingestion_flow(
        conn_fn=conn_fn,
        settings=settings,
    )
    silver.ingestion_flow(
        conn_fn=conn_fn,
        settings=settings,
    )
    gold.ingestion_flow(
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
        database=settings_temp.database(
            name="acidentes",
            db_dir="acidentes",
        ),
    )

    ingestion_flow(conn_fn=conn_fn)
