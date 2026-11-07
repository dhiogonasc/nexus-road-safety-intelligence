from typing import Callable, ContextManager, Dict, List, Optional

import duckdb
from prefect import task

from src.persistence.storage.utils import get_storage_path
from persistence.database.provider import execute
from src.persistence.storage.settings import BucketSettings
from .constants.sql import (
    CREATE_QUERIES_SQL,
    BOOTSTRAP_QUERIES_SQL,
    COPY_TO_PARQUET_QUERIES_SQL,
    UPSERT_BY_PARTITIONS_QUERIES_SQL,
)
from .constants.storage import BASE_PATH
from ..silver.fact.constants.storage import BASE_PATH as SOURCE_BASE_PATH
from ..silver.dimension.constants.storage import (
    BASE_PATH as SOURCE_DIMENSION_BASE_PATH,
)
from .shared.operation import fetch_table_partitions


@task(
    name="create_table",
    task_run_name="create_table: {table_name}",
)
def create_table(
    table_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
):
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=CREATE_QUERIES_SQL[table_name],
        )


@task(
    name="bootstrap_table",
    task_run_name="bootstrap_table: {table_name}",
)
def bootstrap_table(
    table_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    with conn_fn() as conn:
        try:
            execute(
                conn=conn,
                query=BOOTSTRAP_QUERIES_SQL[table_name],
                storage_path=get_storage_path(
                    table_name=table_name,
                    base_path=BASE_PATH,
                    settings=settings,
                ),
            )
        except duckdb.IOException:
            pass


@task(
    name="copy_table_to_parquet",
    task_run_name="copy_table_to_parquet: {table_name}",
)
def copy_table_to_parquet(
    table_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=COPY_TO_PARQUET_QUERIES_SQL[table_name],
            storage_path=get_storage_path(
                table_name=table_name,
                base_path=BASE_PATH,
                settings=settings,
            ),
        )


@task(
    name="_upsert_table",
    task_run_name="_upsert_table: {filter_clause}",
)
def _upsert_table(
    table_name: str,
    source_fact_table: str,
    source_dimension_storage_path: Dict[str, str],
    filter_clause: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):
    with conn_fn() as conn:
        execute(
            conn=conn,
            query=UPSERT_BY_PARTITIONS_QUERIES_SQL[table_name],
            filter_clause=filter_clause,
            source_storage_path=get_storage_path(
                table_name=source_fact_table,
                base_path=SOURCE_BASE_PATH,
                settings=settings,
            ),
            **source_dimension_storage_path,
        )

@task(
    name="upsert_table_by_partitions",
    task_run_name="upsert_table_by_partitions: {table_name}",
)
def upsert_table_by_partitions(
    table_name: str,
    source_fact_table: str,
    source_dimension_tables: List[str],
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    settings: Optional[BucketSettings] = None,
):

    source_dimension_storage_path = {
        f"{dim}_storage_path": get_storage_path(
            table_name=dim,
            base_path=SOURCE_DIMENSION_BASE_PATH,
            settings=settings,
        )
        for dim in source_dimension_tables
    }

    partitions = fetch_table_partitions.submit(
        source_table=source_fact_table,
        source_base_path=SOURCE_BASE_PATH,
        conn_fn=conn_fn,
        settings=settings,
    ).result()

    filter_clauses = [
        " ".join(
            f"AND fato.{k} = {f"'{v}'" if isinstance(v, str) else v}"
            for k, v in partition.items()
        )
        for partition in partitions
    ]

    for filter_clause in filter_clauses:
        _upsert_table(
            table_name=table_name,
            source_fact_table=source_fact_table,
            source_dimension_storage_path=source_dimension_storage_path,
            filter_clause=filter_clause,
            conn_fn=conn_fn,
            settings=settings,
        )