from prefect import flow, unmapped

from src.pipeline.model import ALL_TABLES
from src.pipeline.task.ddl import create_table
from src.persistence.database.provider import DuckDBProvider


@flow(
    name="table_ddl_flow",
    flow_run_name="table_ddl_flow",
)
def ddl_flow(duckdb: DuckDBProvider):
    create_table.map(
        table=ALL_TABLES,
        duckdb=unmapped(duckdb),
    ).result()


if __name__ == "__main__":
    ddl_flow(duckdb=DuckDBProvider())
