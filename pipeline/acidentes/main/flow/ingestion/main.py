from functools import partial
from typing import Callable, ContextManager, Optional

import duckdb
from prefect import flow

from src.persistence.storage.settings import BucketSettings
from src.persistence.database.settings import settings_main
from src.persistence.database.operation import (
    load_extensions,
    attach_connections,
    create_connection,
)
from src.persistence.database.operation import (
    load_extensions,
    create_connection,
)

from .layer import (
    core,
    analytics,
)


@flow(
    name="ingestion_flow",
    flow_run_name="ingestion_flow",
)
def ingestion_flow(
    catalog_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    core.ingestion_flow(
        conn_fn=conn_fn,
        settings=settings,
        catalog_name=catalog_name,
    )
    analytics.ingestion_flow(
        conn_fn=conn_fn,
        settings=settings,
        catalog_name=catalog_name,
    )


if __name__ == "__main__":

    load_extensions_fn = partial(
        load_extensions,
        extensions=["postgres"],
    )
    attach_connections_fn = partial(
        attach_connections,
        connections=[settings_main.attach_config],
    )
    conn_fn = partial(
        create_connection,
        load_extensions_fn=load_extensions_fn,
        attach_connections_fn=attach_connections_fn,
    )

    ingestion_flow(
        conn_fn=conn_fn,
        catalog_name=settings_main.DB_NAME,
    )
