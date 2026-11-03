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
from src.pipeline.acidentes.main.task.ingestion.analytics.constants.summary import (
    TABLES as AGGREGATION_TABLES,
)
from src.pipeline.acidentes.main.task.ingestion.analytics.operation import (
    upsert_table as upsert_aggregation_table,
)


@flow(
    name="aggregation_ingestion_flow",
    flow_run_name="aggregation_ingestion_flow",
)
def aggregation_ingestion_flow(
    catalog_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):

    futures = upsert_aggregation_table.map(
        conn_fn=conn_fn,
        settings=settings,
        catalog_name=catalog_name,
        table_name=AGGREGATION_TABLES,
    )

    for future in futures:
        future.result()


@flow(
    name="ingestion_flow",
    flow_run_name="ingestion_flow",
)
def ingestion_flow(
    catalog_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    aggregation_ingestion_flow(
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
