from prefect import flow, task, unmapped

from src.pipeline.acidentes.temp.task.ingestion.bronze.operation import (
    bronze_storage_factory,
)
from src.persistence.database.provider import DuckDBProvider

from src.pipeline.acidentes.temp.task.ingestion.silver.staging.constants.summary import (
    TABLES as STAGING_TABLES,
)
from src.pipeline.acidentes.temp.task.ingestion.silver.dimension.constants.summary import (
    TABLES as DIMENSION_TABLES,
)
from src.pipeline.acidentes.temp.task.ingestion.silver.fact.constants.summary import (
    TABLES as FACT_TABLES,
)

from src.pipeline.acidentes.temp.task.ingestion.silver.staging.operation import (
    stage_table,
    log_table_charge,
    copy_table_to_parquet,
    staging_storage_factory,
)
from src.pipeline.acidentes.temp.task.ingestion.silver.dimension.operation import (
    upsert_table as upsert_dimension_table,
    create_table as create_dimension_table,
    bootstrap_table as bootstrap_dimension_table,
    copy_table_to_parquet as copy_dimension_table_to_parquet,
    dimension_storage_factory,
)
from src.pipeline.acidentes.temp.task.ingestion.silver.fact.operation import (
    create_table as create_fact_table,
    log_table_charge as log_fact_charge,
    bootstrap_table as bootstrap_fact_table,
    copy_table_to_parquet as copy_fact_table_to_parquet,
    upsert_table_by_partitions as upsert_fact_by_partitions,
    fact_storage_factory,
)


@flow(
    name="staging_ingestion_flow",
    flow_run_name="staging_ingestion_flow",
)
def staging_ingestion_flow(duckdb: DuckDBProvider):
    storage_list = staging_storage_factory.map(
        table=STAGING_TABLES,
    ).result()

    source_storage_list = bronze_storage_factory.map(
        table=[table.source for table in STAGING_TABLES]
    ).result()

    stage_table.map(
        table=STAGING_TABLES,
        source_storage=source_storage_list,
        duckdb=unmapped(duckdb),
    ).result()

    copy_table_to_parquet.map(
        table=STAGING_TABLES,
        storage=storage_list,
        duckdb=unmapped(duckdb),
    ).result()

    log_table_charge.map(
        table=STAGING_TABLES,
        storage=storage_list,
        duckdb=unmapped(duckdb),
    ).result()


@flow(
    name="dimension_ingestion_flow",
    flow_run_name="dimension_ingestion_flow",
)
def dimension_ingestion_flow(duckdb: DuckDBProvider):
    storage_list = dimension_storage_factory.map(
        table=DIMENSION_TABLES,
    ).result()

    create_dimension_table.map(
        table=DIMENSION_TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    bootstrap_dimension_table.map(
        table=DIMENSION_TABLES,
        storage=storage_list,
        duckdb=unmapped(duckdb),
    ).result()

    upsert_dimension_table.map(
        table=DIMENSION_TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    copy_dimension_table_to_parquet.map(
        table=DIMENSION_TABLES,
        storage=storage_list,
        duckdb=unmapped(duckdb),
    ).result()


@flow(
    name="fact_ingestion_flow",
    flow_run_name="fact_ingestion_flow",
)
def fact_ingestion_flow(duckdb: DuckDBProvider):
    storage_list = fact_storage_factory.map(
        table=FACT_TABLES,
    ).result()

    source_storage_list = staging_storage_factory.map(
        table=[table.source for table in FACT_TABLES]
    ).result()

    create_fact_table.map(
        table=FACT_TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    bootstrap_fact_table.map(
        table=FACT_TABLES,
        storage=storage_list,
        duckdb=unmapped(duckdb),
    ).result()

    upsert_fact_by_partitions.map(
        table=FACT_TABLES,
        duckdb=unmapped(duckdb),
        source_storage=source_storage_list,
    ).result()

    copy_fact_table_to_parquet.map(
        table=FACT_TABLES,
        storage=storage_list,
        duckdb=unmapped(duckdb),
    ).result()

    log_fact_charge.map(
        table=FACT_TABLES,
        storage=storage_list,
        duckdb=unmapped(duckdb),
    ).result()


@flow(
    name="silver_ingestion_flow",
    flow_run_name="silver_ingestion_flow",
)
def ingestion_flow(duckdb: DuckDBProvider):
    staging_ingestion_flow(duckdb=duckdb)
    dimension_ingestion_flow(duckdb=duckdb)
    fact_ingestion_flow(duckdb=duckdb)


if __name__ == "__main__":
    ingestion_flow(duckdb=DuckDBProvider())
