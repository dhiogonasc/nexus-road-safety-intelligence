from duckdb import IOException
from prefect import task

from ..sql.ingestion import *
from ..model import BaseTable
from src.persistence.database.provider import DuckDBProvider


@task(
    name="stage_raw",
    task_run_name="stage_raw: {table.name}",
)
def stage_raw(
    table: BaseTable,
    duckdb: DuckDBProvider,
    delim: str = ";",
    encoding: str = "latin-1",
):
    duckdb.execute_query(
        sql=STAGE_SQL[table.name],
        source_data_path=table.source,
        delim=delim,
        encoding=encoding,
    )


@task(
    name="stage_table",
    task_run_name="stage_table: {table.name}",
)
def stage_table(
    table: BaseTable,
    duckdb: DuckDBProvider,
):
    base_source = table.source.base
    source_path = {
        key: value
        for key, value in {
            f"{base_source.table_name}_storage_path": base_source.get_storage_path(),
            f"{base_source.table_name}_log_path": base_source.get_log_path(),
        }.items()
    }

    duckdb.execute_query(
        sql=STAGE_SQL[table.name],
        **source_path,
    )


@task(
    name="copy_table_to_parquet",
    task_run_name="copy_table_to_parquet: {table.name}",
)
def copy_table_to_parquet(
    table: BaseTable,
    duckdb: DuckDBProvider,
):
    duckdb.execute_query(
        sql=COPY_TO_PARQUET_SQL[table.name],
        storage_path=table.storage.get_storage_path(),
    )


@task(
    name="log_table_charge",
    task_run_name="log_table_charge: {table.name}",
)
def log_table_charge(
    table: BaseTable,
    duckdb: DuckDBProvider,
):
    duckdb.execute_query(
        sql=LOG_CHARGE_SQL[table.name],
        log_path=table.storage.get_log_path(),
    )


@task(
    name="bootstrap_table",
    task_run_name="bootstrap_table: {table.name}",
)
def bootstrap_table(
    table: BaseTable,
    duckdb: DuckDBProvider,
):
    try:
        return duckdb.execute_query(
            sql=BOOTSTRAP_SQL[table.name],
            storage_path=table.storage.get_storage_path(),
        )
    except IOException:
        pass


@task(
    name="upsert_table",
    task_run_name="upsert_table: {table.name}",
)
def upsert_table(
    table: BaseTable,
    duckdb: DuckDBProvider,
):
    base_source = table.source.base
    source_path = {
        f"{base_source.table_name}_storage_path": base_source.get_storage_path()
    }

    return duckdb.execute_query(
        sql=UPSERT_SQL[table.name],
        **source_path,
    )


@task(
    name="_fetch_table_partitions",
    task_run_name="_fetch_table_partitions",
)
def _fetch_table_partitions(
    table: BaseTable,
    duckdb: DuckDBProvider,
):
    base_source = table.source.base
    return duckdb.fecth_df(
        sql=SHARED_SQL["fetch_partitions"],
        source_log_path=base_source.get_log_path(),
    ).to_dict(orient="records")


@task(
    name="_upsert_partition",
    task_run_name="_upsert_partition: {filter_clause}",
)
def _upsert_partition(
    table: BaseTable,
    filter_clause: str,
    duckdb: DuckDBProvider,
):
    source_storage_path = {
        f"{source.table_name}_storage_path": source.get_storage_path()
        for source in table.source.all
    }

    return duckdb.execute_query(
        sql=UPSERT_BY_PARTITIONS_SQL[table.name],
        filter_clause=filter_clause,
        **source_storage_path,
    )


@task(
    name="upsert_table_by_partitions",
    task_run_name="upsert_table_by_partitions: {table.name}",
)
def upsert_table_by_partitions(
    table: BaseTable,
    duckdb: DuckDBProvider,
):
    partitions = _fetch_table_partitions.submit(
        duckdb=duckdb,
        table=table,
    ).result()

    filter_clauses = []
    for partition in partitions:
        conditions = []
        for k, v in partition.items():
            formatted_val = f"'{v}'" if isinstance(v, str) else v
            conditions.append(f"AND {k} = {formatted_val}")

        filter_clauses.append(" ".join(conditions))

    for filter_clause in filter_clauses:
        _upsert_partition(
            table=table,
            filter_clause=filter_clause,
            duckdb=duckdb,
        )
