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
    source: StorageProvider,
):
    return duckdb.fecth_df(
        sql=SHARED_QUERIES_SQL["fetch_partitions"],
        source_log_path=source.get_log_path(),
    ).to_dict(orient="records")
