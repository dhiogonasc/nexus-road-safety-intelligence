from duckdb import IOException
from prefect import task

from .constants.sql import (
    CREATE_QUERIES_SQL,
    BOOTSTRAP_QUERIES_SQL,
    LOG_CHARGE_QUERIES_SQL,
    COPY_TO_PARQUET_QUERIES_SQL,
    UPSERT_BY_PARTITIONS_QUERIES_SQL,
)
from .constants.storage import BASE_PATH
from .constants.summary import GoldTable
from src.persistence.database.provider import DuckDBProvider
from src.persistence.storage.provider import StorageProvider
from .shared.operation import fetch_table_partitions


@task(
    name="bootstrap_table",
    task_run_name="bootstrap_table: {table.name}",
)
def bootstrap_table(
    table: GoldTable,
    duckdb: DuckDBProvider,
    storage: StorageProvider,
):
    try:
        return duckdb.execute_query(
            sql=BOOTSTRAP_QUERIES_SQL[table.name],
            storage_path=storage.get_storage_path(),
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
    storage: StorageProvider,
):
    return duckdb.execute_query(
        sql=COPY_TO_PARQUET_QUERIES_SQL[table.name],
        storage_path=storage.get_storage_path(),
    )


@task(
    name="create_table",
    task_run_name="create_table: {table.name}",
)
def create_table(
    table: GoldTable,
    duckdb: DuckDBProvider,
):
    return duckdb.execute_query(sql=CREATE_QUERIES_SQL[table.name])


@task(
    name="log_table_charge",
    task_run_name="log_table_charge: {table.name}",
)
def log_table_charge(
    table: GoldTable,
    duckdb: DuckDBProvider,
    storage: StorageProvider,
):
    return duckdb.execute_query(
        sql=LOG_CHARGE_QUERIES_SQL[table.name],
        log_path=storage.get_log_path(),
    )


@task(
    name="_upsert_partition",
    task_run_name="_upsert_partition: {filter_clause}",
)
def _upsert_partition(
    table: GoldTable,
    filter_clause: str,
    duckdb: DuckDBProvider,
    source_storage: StorageProvider,
):
    return duckdb.execute_query(
        sql=UPSERT_BY_PARTITIONS_QUERIES_SQL[table.name],
        filter_clause=filter_clause,
        source_storage_path=source_storage.get_storage_path(),
    )


@task(
    name="upsert_table_by_partitions",
    task_run_name="upsert_table_by_partitions: {table.name}",
)
def upsert_table_by_partitions(
    table: GoldTable,
    duckdb: DuckDBProvider,
    source_storage: StorageProvider,
):
    partitions = fetch_table_partitions.submit(
        duckdb=duckdb,
        source_storage=source_storage,
    ).result()

    filter_clauses = [
        " ".join(
            f"AND {k} = {f"'{v}'" if isinstance(v, str) else v}"
            for k, v in partition.items()
        )
        for partition in partitions
    ]

    for filter_clause in filter_clauses:
        _upsert_partition(
            table=table,
            filter_clause=filter_clause,
            duckdb=duckdb,
            source_storage=source_storage,
        )


@task(
    name="fact_storage_factory",
    task_run_name="fact_storage_factory: {table.name}",
)
def fact_storage_factory(
    table: GoldTable,
):
    return StorageProvider(
        table_name=table.name,
        base_path=BASE_PATH,
    )
