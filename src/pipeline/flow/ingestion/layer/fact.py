from prefect import flow, unmapped

from src.persistence.database.provider import DuckDBProvider
from src.pipeline.model import FCT_TABLES
from src.pipeline.task.ingestion import (
    create_table,
    bootstrap_table,
    upsert_table_by_partitions,
    copy_table_to_parquet,
    log_table_charge,
)


@flow(
    name="fact_ingestion_flow",
    flow_run_name="fact_ingestion_flow",
)
def ingestion_flow(duckdb: DuckDBProvider):
    create_table.map(
        table=FCT_TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    bootstrap_table.map(
        table=FCT_TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    upsert_table_by_partitions.map(
        table=FCT_TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    copy_table_to_parquet.map(
        table=FCT_TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    log_table_charge.map(
        table=FCT_TABLES,
        duckdb=unmapped(duckdb),
    ).result()


if __name__ == "__main__":
    ingestion_flow(duckdb=DuckDBProvider())
