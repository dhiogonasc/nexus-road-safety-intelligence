from prefect import flow

from src.persistence.database.provider import DuckDBProvider
from .ddl.main import ddl_flow
from .ingestion.main import ingestion_flow


@flow(
    name="ingestion_flow",
    flow_run_name="ingestion_flow",
)
def main_flow(duckdb: DuckDBProvider):
    ddl_flow(duckdb=duckdb)
    ingestion_flow(duckdb=duckdb)


if __name__ == "__main__":
    main_flow(duckdb=DuckDBProvider())
