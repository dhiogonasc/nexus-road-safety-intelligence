from prefect import task

from .constants.sql import SHARED_QUERIES_SQL
from src.persistence.database.provider import DuckDBProvider
from src.persistence.storage.provider import StorageProvider


@task(
    name="fetch_table_partitions",
    task_run_name="fetch_table_partitions",
)
def fetch_table_partitions(
    duckdb: DuckDBProvider,
    source_storage: StorageProvider,
):
    print(f"source_storage logs: {source_storage.get_log_path()}")
    result = duckdb.execute_query(
        sql=SHARED_QUERIES_SQL["fetch_partitions"],
        source_log_path=source_storage.get_log_path(),
    )

    keys = [desc[0] for desc in result.description]
    values = dict.fromkeys(result.fetchall()).keys()

    return [dict(zip(keys, values_row)) for values_row in values]
