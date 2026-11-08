from prefect import flow, unmapped

from src.persistence.database.provider import DuckDBProvider
from src.pipeline.temp.task.ingestion.bronze.constants.summary import TABLES
from src.pipeline.temp.task.ingestion.bronze.operation import (
    copy_table_to_parquet,
    log_table_charge,
    stage_table,
)


@flow(
    name="bronze_ingestion_flow",
    flow_run_name="bronze_ingestion_flow",
)
def ingestion_flow(duckdb: DuckDBProvider):
    stage_table.map(
        table=TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    copy_table_to_parquet.map(
        table=TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    log_table_charge.map(
        table=TABLES,
        duckdb=unmapped(duckdb),
    ).result()


if __name__ == "__main__":
    ingestion_flow(duckdb=DuckDBProvider())
