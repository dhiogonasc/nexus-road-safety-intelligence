from functools import partial
from typing import Callable, ContextManager, List, Optional

import duckdb
from griffe import load_extensions
from prefect import flow

from src.persistence.storage.settings import BucketSettings
from src.persistence.database.settings import (
    settings_temp,
    settings_main,
)
from src.persistence.database.operation import (
    load_extensions,
    attach_connections,
    create_connection,
)


from src.pipeline.acidentes.temp.ddl.operation import create_schema

from src.pipeline.acidentes.main.ingestion.analytics.operation import (
    upsert as upsert_analytics,
    ANALYTICS_TABLES,
)


@flow(
    name="analytics_ingestion_flow",
    flow_run_name="analytics_ingestion_flow",
)
def analytics_ingestion_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    catalog_name: str,
    settings: Optional[BucketSettings] = None,
):
    futures = upsert_analytics.map(
        conn_fn=conn_fn,
        table_name=ANALYTICS_TABLES,
        catalog_name=catalog_name,
        settings=settings,
    )

    for future in futures:
        future.result()


@flow(
    name="ingestion_flow",
    flow_run_name="ingestion_flow",
)
def ingestion_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    catalog_name: str,
    settings: Optional[BucketSettings] = None,
):
    analytics_ingestion_flow(
        conn_fn=conn_fn,
        catalog_name=catalog_name,
        settings=settings,
    )


if __name__ == "__main__":
    load_extensions_fn = partial(
        load_extensions,
        extensions=[
            "postgres",
            "httpfs",
            "parquet",
        ],
    )
    attach_connections_fn = partial(
        attach_connections,
        connections=[
            {
                "string": settings_main.conn_string,
                "alias": settings_main.DB_NAME,
                "option": "(TYPE POSTGRES)",
            }
        ],
    )
    conn_fn = partial(
        create_connection,
        load_extensions_fn=load_extensions_fn,
        attach_connections_fn=attach_connections_fn,
        database=settings_temp.database(
            name="acidentes",
            db_dir="acidentes",
        ),
    )

    ingestion_flow(
        conn_fn=conn_fn,
        catalog_name=settings_main.DB_NAME,
    )
