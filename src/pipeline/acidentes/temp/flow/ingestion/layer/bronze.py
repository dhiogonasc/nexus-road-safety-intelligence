from prefect import flow, unmapped

from src.persistence.database.provider import DuckDBProvider
from src.pipeline.acidentes.temp.task.ingestion.bronze.constants.summary import TABLES
from src.pipeline.acidentes.temp.task.ingestion.bronze.operation import (
    stage_table,
    log_table_charge,
    copy_table_to_parquet,
    bronze_storage_factory,
)


@flow(
    name="bronze_ingestion_flow",
    flow_run_name="bronze_ingestion_flow",
)
def ingestion_flow(duckdb: DuckDBProvider):
    storage_list = bronze_storage_factory.map(
        table=TABLES,
    ).result()

    stage_table.map(
        table=TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    copy_table_to_parquet.map(
        table=TABLES,
        storage=storage_list,
        duckdb=unmapped(duckdb),
    ).result()

    log_table_charge.map(
        table=TABLES,
        storage=storage_list,
        duckdb=unmapped(duckdb),
    ).result()


if __name__ == "__main__":
    ingestion_flow(duckdb=DuckDBProvider())
