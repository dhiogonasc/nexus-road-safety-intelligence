from prefect import flow

from src.persistence.database.provider import DuckDBProvider
from .layer import (
    raw,
    staging,
    dimension,
    fact,
    aggregation,
)


@flow(
    name="ingestion_flow",
    flow_run_name="ingestion_flow",
)
def ingestion_flow(duckdb: DuckDBProvider):
    raw.ingestion_flow(duckdb=duckdb)
    staging.ingestion_flow(duckdb=duckdb)
    dimension.ingestion_flow(duckdb=duckdb)
    fact.ingestion_flow(duckdb=duckdb)
    aggregation.ingestion_flow(duckdb=duckdb)


if __name__ == "__main__":
    ingestion_flow(duckdb=DuckDBProvider())
