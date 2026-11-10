from prefect import flow, unmapped

from src.persistence.database.provider import DuckDBProvider
from src.pipeline.model import AGG_TABLES
from src.pipeline.task.ingestion import (
    create_table,
    bootstrap_table,
    upsert_table_by_partitions,
    copy_table_to_parquet,
)


@flow(
    name="aggregation_ingestion_flow",
    flow_run_name="aggregation_ingestion_flow",
)
def ingestion_flow(duckdb: DuckDBProvider):
    create_table.map(
        table=AGG_TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    bootstrap_table.map(
        table=AGG_TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    upsert_table_by_partitions.map(
        table=AGG_TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    copy_table_to_parquet.map(
        table=AGG_TABLES,
        duckdb=unmapped(duckdb),
    ).result()


if __name__ == "__main__":
    ingestion_flow(duckdb=DuckDBProvider())
