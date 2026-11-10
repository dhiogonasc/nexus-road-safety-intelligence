from prefect import task

from ..sql.ddl import *
from ..model import BaseTable
from src.persistence.database.provider import DuckDBProvider


@task(
    name="create_schema",
    task_run_name="create_schema: {schema_name}",
)
def create_schema(
    schema_name: str,
    duckdb: DuckDBProvider,
):
    return duckdb.execute_query(sql=SCHEMA_SQL[schema_name])


@task(
    name="create_table",
    task_run_name="create_table: {table.name}",
)
def create_table(
    table: BaseTable,
    duckdb: DuckDBProvider,
):
    return duckdb.execute_query(sql=TABLE_SQL[table.name])
