from prefect import task

from src.persistence.database.provider import DuckDBProvider
from .constants.sql import QUERIES_SQL


@task(
    name="create_schema",
    task_run_name="create_schema: {schema_name}",
)
def create_schema(
    catalog_name: str,
    schema_name: str,
    duckdb: DuckDBProvider,
):
    duckdb.execute_query(
        sql=QUERIES_SQL["create_schema"],
        catalog_name=catalog_name,
        schema_name=schema_name,
    )
