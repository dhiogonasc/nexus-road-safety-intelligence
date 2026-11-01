from functools import partial
from typing import Callable, ContextManager, Optional

import duckdb

from src.persistence.database.settings import settings
from src.persistence.database.operation import create_connection, load_extensions
from src.persistence.storage.settings import BucketSettings

from .ddl.schema import schema_ddl_flow, SCHEMAS
from .ingestion.clean import clean_ingestion_flow
from .ingestion.raw import raw_ingestion_flow
from .ingestion.aggregation import aggregation_ingestion_flow


def main_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    schema_ddl_flow(
        conn_fn=conn_fn,
        schemas=SCHEMAS,
    )
    raw_ingestion_flow(
        conn_fn=conn_fn,
        settings=settings,
    )
    clean_ingestion_flow(
        conn_fn=conn_fn,
        settings=settings,
    )
    aggregation_ingestion_flow(
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
        database=settings.database(
            name="acidentes",
            db_dir="acidentes",
        ),
    )

    main_flow(conn_fn=conn_fn)
