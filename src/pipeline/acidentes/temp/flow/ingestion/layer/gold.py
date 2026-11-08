from prefect import flow, unmapped

from src.pipeline.acidentes.temp.task.ingestion.gold.constants.summary import TABLES
from src.pipeline.acidentes.temp.task.ingestion.gold.operation import (
    create_table,
    bootstrap_table,
    copy_table_to_parquet,
    upsert_table_by_partitions,
)
from src.persistence.database.provider import DuckDBProvider


@flow(
    name="gold_ingestion_flow",
    flow_run_name="gold_ingestion_flow",
)
def ingestion_flow(duckdb: DuckDBProvider):
    create_table.map(
        table=TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    bootstrap_table.map(
        table=TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    upsert_table_by_partitions.map(
        table=TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    copy_table_to_parquet.map(
        table=TABLES,
        duckdb=unmapped(duckdb),
    ).result()


if __name__ == "__main__":
    ingestion_flow(duckdb=DuckDBProvider())
