from prefect import flow

from src.persistence.database.provider import DuckDBProvider
from .layer import schema, table


@flow(
    name="ingestion_flow",
    flow_run_name="ingestion_flow",
)
def ddl_flow(duckdb: DuckDBProvider):
    schema.ddl_flow(duckdb=duckdb)
    table.ddl_flow(duckdb=duckdb)


if __name__ == "__main__":
    ddl_flow(duckdb=DuckDBProvider())
