from prefect import flow

from .layer import (
    silver,
)
from src.persistence.database.provider import DuckDBProvider

from .layer import bronze
from .layer import gold


@flow(
    name="ingestion_flow",
    flow_run_name="ingestion_flow",
)
def ingestion_flow(duckdb: DuckDBProvider):
    bronze.ingestion_flow(duckdb=duckdb)
    silver.ingestion_flow(duckdb=duckdb)
    gold.ingestion_flow(duckdb=duckdb)


if __name__ == "__main__":
    ingestion_flow(duckdb=DuckDBProvider())
