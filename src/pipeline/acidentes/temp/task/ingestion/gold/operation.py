from duckdb import IOException
from prefect import task

from .constants.sql import (
    CREATE_QUERIES_SQL,
    BOOTSTRAP_QUERIES_SQL,
    COPY_TO_PARQUET_QUERIES_SQL,
    UPSERT_BY_PARTITIONS_QUERIES_SQL,
)
from .constants.summary import GoldTable
from .shared.operation import fetch_table_partitions
from src.persistence.database.provider import DuckDBProvider


@task(
    name="bootstrap_table",
    task_run_name="bootstrap_table: {table.name}",
)
def bootstrap_table(
    table: GoldTable,
    duckdb: DuckDBProvider,
):
    try:
        duckdb.execute_query(
            sql=BOOTSTRAP_QUERIES_SQL[table.name],
            storage_path=table.storage.get_storage_path(),
        )
    except IOException:
        pass


@task(
    name="copy_table_to_parquet",
    task_run_name="copy_table_to_parquet: {table.name}",
)
def copy_table_to_parquet(
    table: GoldTable,
    duckdb: DuckDBProvider,
):
    duckdb.execute_query(
        sql=COPY_TO_PARQUET_QUERIES_SQL[table.name],
        storage_path=table.storage.get_storage_path(),
    )


@task(
    name="create_table",
    task_run_name="create_table: {table.name}",
)
def create_table(
    table: GoldTable,
    duckdb: DuckDBProvider,
):
    duckdb.execute_query(sql=CREATE_QUERIES_SQL[table.name])


@task(
    name="_upsert_partition",
    task_run_name="_upsert_partition: {filter_clause}",
)
def _upsert_partition(
    table: GoldTable,
    filter_clause: str,
    duckdb: DuckDBProvider,
):
    source_storage_path = {
        f"{source.table_name}_storage_path": source.get_storage_path()
        for source in table.all_sources
    }

    duckdb.execute_query(
        sql=UPSERT_BY_PARTITIONS_QUERIES_SQL[table.name],
        filter_clause=filter_clause,
        **source_storage_path,
    )


@task(
    name="upsert_table_by_partitions",
    task_run_name="upsert_table_by_partitions: {table.name}",
)
def upsert_table_by_partitions(
    table: GoldTable,
    duckdb: DuckDBProvider,
):

    partitions = fetch_table_partitions.submit(
        duckdb=duckdb,
        source=table.fact,
    ).result()

    filter_clauses = []
    for partition in partitions:
        conditions = []
        for k, v in partition.items():
            formatted_val = f"'{v}'" if isinstance(v, str) else v
            conditions.append(f"AND fato.{k} = {formatted_val}")
        filter_clauses.append(" ".join(conditions))

    for filter_clause in filter_clauses:
        _upsert_partition(
            table=table,
            filter_clause=filter_clause,
            duckdb=duckdb,
        )
