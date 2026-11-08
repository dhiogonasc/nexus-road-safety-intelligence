from prefect import task

from .constants.sql import QUERIES_SQL
from src.persistence.database.provider import DuckDBProvider


@task(
    name="create_table",
    task_run_name="create_table: {table}",
)
def create_table(
    table: str,
    catalog_name: str,
    duckdb: DuckDBProvider,
):
    duckdb.execute_query(
        catalog_name=catalog_name,
        sql=QUERIES_SQL[table],
    )
