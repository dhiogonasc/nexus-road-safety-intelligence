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

from src.pipeline.acidentes.temp.task.ingestion.silver.staging.constants.summary import (
    TABLES as STAGING_TABLES,
)
from src.pipeline.acidentes.temp.task.ingestion.silver.dimension.constants.summary import (
    TABLES as DIMENSION_TABLES,
)
from src.pipeline.acidentes.temp.task.ingestion.silver.fact.constants.summary import (
    TABLES as FACT_TABLES,
)

from src.pipeline.acidentes.temp.task.ingestion.silver.staging.operation import (
    stage_table,
    log_table_charge,
    copy_table_to_parquet,
)
from src.pipeline.acidentes.temp.task.ingestion.silver.dimension.operation import (
    upsert_table as upsert_dimension_table,
    create_table as create_dimension_table,
    bootstrap_table as bootstrap_dimension_table,
    copy_table_to_parquet as copy_dimension_table_to_parquet,
)
from src.pipeline.acidentes.temp.task.ingestion.silver.fact.operation import (
    upsert_table_by_partitions,
    create_table as create_fact_table,
    log_table_charge as log_fact_charge,
    bootstrap_table as bootstrap_fact_table,
    copy_table_to_parquet as copy_fact_table_to_parquet,
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

    table_name_list = [item["table_name"] for item in STAGING_TABLES]
    source_table_list = [item["source_table"] for item in STAGING_TABLES]

    stage_futures = stage_table.map(
        table_name=table_name_list,
        source_table=source_table_list,
        conn_fn=conn_fn,
        settings=settings,
    )

    log_futures = log_table_charge.map(
        table_name=table_name_list,
        conn_fn=conn_fn,
        settings=settings,
        wait_for=stage_futures,
    )
    storage_futures.append(log_futures)

    copy_futures = copy_table_to_parquet.map(
        table_name=table_name_list,
        conn_fn=conn_fn,
        settings=settings,
        wait_for=stage_futures,
    )
    storage_futures.append(copy_futures)

    for future_list in storage_futures:
        for future in future_list:
            future.result()


@flow(
    name="dimension_ingestion_flow",
    flow_run_name="dimension_ingestion_flow",
)
def dimension_ingestion_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    create_futures = create_dimension_table.map(
        table_name=DIMENSION_TABLES,
        conn_fn=conn_fn,
        wait_for=[],
    )

    bootstrap_futures = bootstrap_dimension_table.map(
        table_name=DIMENSION_TABLES,
        conn_fn=conn_fn,
        settings=settings,
        wait_for=create_futures,
    )

    upsert_futures = upsert_dimension_table.map(
        table_name=DIMENSION_TABLES,
        conn_fn=conn_fn,
        wait_for=bootstrap_futures,
    )

    copy_futures = copy_dimension_table_to_parquet.map(
        table_name=DIMENSION_TABLES,
        conn_fn=conn_fn,
        settings=settings,
        wait_for=upsert_futures,
    )

    for future in copy_futures:
        future.result()


@flow(
    name="fact_ingestion_flow",
    flow_run_name="fact_ingestion_flow",
)
def fact_ingestion_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    table_name_list = [item["table_name"] for item in FACT_TABLES]
    source_table_list = [item["source_table"] for item in FACT_TABLES]

    create_futures = create_fact_table.map(
        table_name=table_name_list,
        conn_fn=conn_fn,
        wait_for=[],
    )

    bootstrap_futures = bootstrap_fact_table.map(
        table_name=table_name_list,
        conn_fn=conn_fn,
        settings=settings,
        wait_for=create_futures,
    )

    upsert_futures = upsert_table_by_partitions.map(
        table_name=table_name_list,
        source_table=source_table_list,
        conn_fn=conn_fn,
        wait_for=bootstrap_futures,
    )

    storage_futures = []

    log_futures = log_fact_charge.map(
        table_name=table_name_list,
        conn_fn=conn_fn,
        settings=settings,
        wait_for=upsert_futures,
    )
    storage_futures.append(log_futures)

    copy_futures = copy_fact_table_to_parquet.map(
        table_name=table_name_list,
        conn_fn=conn_fn,
        settings=settings,
        wait_for=upsert_futures,
    )
    storage_futures.append(copy_futures)
    
    for future_list in storage_futures:
        for future in future_list:
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
    dimension_ingestion_flow(
        conn_fn=conn_fn,
        settings=settings,
    )
    fact_ingestion_flow(
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
