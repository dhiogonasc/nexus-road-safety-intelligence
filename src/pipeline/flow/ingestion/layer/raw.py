from prefect import flow, unmapped

from src.persistence.database.provider import DuckDBProvider
from src.pipeline.model import RAW_TABLES
from src.pipeline.task.ingestion import (
    copy_table_to_parquet,
    log_table_charge,
    stage_raw,
)


@flow(
    name="raw_ingestion_flow",
    flow_run_name="raw_ingestion_flow",
)
def ingestion_flow(duckdb: DuckDBProvider):
    stage_raw.map(
        table=RAW_TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    copy_table_to_parquet.map(
        table=RAW_TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    log_table_charge.map(
        table=RAW_TABLES,
        duckdb=unmapped(duckdb),
    ).result()


if __name__ == "__main__":
    ingestion_flow(duckdb=DuckDBProvider())
