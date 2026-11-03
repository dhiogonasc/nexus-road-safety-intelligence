from functools import partial
from typing import Callable, ContextManager, Optional

import duckdb
from prefect import flow

from src.persistence.storage.settings import BucketSettings
from src.persistence.database.settings import settings_temp
from src.persistence.database.operation import (
    load_extensions,
    create_connection,
)

from src.pipeline.acidentes.temp.task.ingestion.gold.staging.constants.name import (
    STAGING_TABLES,
)
from src.pipeline.acidentes.temp.task.ingestion.gold.staging.operation import (
    stage_table,
    log_table_charge,
    copy_table_to_parquet,
)

from src.pipeline.acidentes.temp.task.ingestion.gold.aggregation.constants.name import (
    AGGREGATION_TABLES,
)
from src.pipeline.acidentes.temp.task.ingestion.gold.aggregation.operation import (
    create_table as create_aggregation_table,
    bootstrap_table as bootstrap_aggregation_table,
    upsert_table as upsert_aggregation_table,
    copy_table_to_parquet as copy_aggregation_table_to_parquet,
)

@flow(
    name="staging_ingestion_flow",
    flow_run_name="staging_ingestion_flow",
)
def staging_ingestion_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    storage_futures = []

    target_tables = [item["target"] for item in STAGING_TABLES]
    source_tables = [item["source"] for item in STAGING_TABLES]

    stage_futures = stage_table.map(
        target_table=target_tables,
        source_table=source_tables,
        conn_fn=conn_fn,
        settings=settings,
    )

    log_futures = log_table_charge.map(
        target_table=target_tables,
        conn_fn=conn_fn,
        settings=settings,
        wait_for=stage_futures,
    )
    storage_futures.append(log_futures)

    copy_futures = copy_table_to_parquet.map(
        target_table=target_tables,
        conn_fn=conn_fn,
        settings=settings,
        wait_for=stage_futures,
    )
    storage_futures.append(copy_futures)

    for future_list in storage_futures:
        for future in future_list:
            future.result()


@flow(
    name="aggregation_ingestion_flow",
    flow_run_name="aggregation_ingestion_flow",
)
def aggregation_ingestion_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    create_futures = create_aggregation_table.map(
        table_name=AGGREGATION_TABLES,
        conn_fn=conn_fn,
        wait_for=[],
    )

    bootstrap_futures = bootstrap_aggregation_table.map(
        table_name=AGGREGATION_TABLES,
        conn_fn=conn_fn,
        settings=settings,
        wait_for=create_futures,
    )

    upsert_futures = upsert_aggregation_table.map(
        table_name=AGGREGATION_TABLES,
        conn_fn=conn_fn,
        wait_for=bootstrap_futures,
    )

    copy_futures = copy_aggregation_table_to_parquet.map(
        table_name=AGGREGATION_TABLES,
        conn_fn=conn_fn,
        settings=settings,
        wait_for=upsert_futures,
    )

    for future in copy_futures:
        future.result()


@flow(
    name="ingestion_flow",
    flow_run_name="ingestion_flow",
)
def ingestion_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    staging_ingestion_flow(
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
        database=settings_temp.database(
            name="acidentes",
            db_dir="acidentes",
        ),
    )

    ingestion_flow(conn_fn=conn_fn)
