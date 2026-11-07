from functools import partial
from typing import Callable, ContextManager, List, Optional

import duckdb
from prefect import flow, task

from src.persistence.storage.settings import BucketSettings
from src.persistence.database.settings import settings_temp
from persistence.database.provider import (
    load_extensions,
    create_connection,
)

from src.pipeline.acidentes.temp.task.ingestion.gold.constants.summary import TABLES
from src.pipeline.acidentes.temp.task.ingestion.gold.operation import (
    create_table,
    bootstrap_table,
    copy_table_to_parquet,
    upsert_table_by_partitions,
)


@task(
    name="_gold_ingestion_flow_factory",
    task_run_name="_gold_ingestion_flow_factory: {table_name}",
)
def _ingestion_flow_factory(
    table_name: str,
    source_fact_table: str,
    source_dimension_tables: List[str],
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    create_future = create_table.submit(
        table_name=table_name,
        conn_fn=conn_fn,
        wait_for=[],
    )

    bootstrap_future = bootstrap_table.submit(
        table_name=table_name,
        conn_fn=conn_fn,
        settings=settings,
        wait_for=[create_future],
    )

    upsert_futures = upsert_table_by_partitions.submit(
        table_name=table_name,
        source_fact_table=source_fact_table,
        source_dimension_tables=source_dimension_tables,
        conn_fn=conn_fn,
        wait_for=[bootstrap_future],
    )

    copy_future = copy_table_to_parquet.submit(
        table_name=table_name,
        conn_fn=conn_fn,
        settings=settings,
        wait_for=[upsert_futures],
    )

    copy_future.result()


@flow(
    name="gold_ingestion_flow",
    flow_run_name="gold_ingestion_flow",
)
def ingestion_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    table_name_list = [item["table_name"] for item in TABLES]
    source_fact_table_list = [item["source_fact_table"] for item in TABLES]
    source_dimension_tables_lists = [item["source_dimension_tables"] for item in TABLES]

    futures = _ingestion_flow_factory.map(
        conn_fn=conn_fn,
        table_name=table_name_list,
        source_fact_table=source_fact_table_list,
        source_dimension_tables=source_dimension_tables_lists,
        settings=settings,
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
