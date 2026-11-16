from prefect import flow, unmapped

from src.model import (
    AGG_TABLES,
    DIM_TABLES,
    FCT_TABLES,
    RAW_TABLES,
    STG_TABLES,
    SCHEMAS,
)
from src.persistence.database import DuckDBProvider
from .task import (
    create_schema,
    create_table,
    bootstrap_table,
    copy_table_to_parquet,
    log_table_charge,
    stage_raw,
    stage_table,
    upsert_table_by_partitions,
    upsert_table,
)


@flow(
    name="schema_ddl_flow",
    flow_run_name="schema_ddl_flow",
)
def ddl_flow(duckdb: DuckDBProvider):
    create_schema.map(
        schema_name=SCHEMAS,
        duckdb=unmapped(duckdb),
    ).result()


@flow(
    name="raw_ingestion_flow",
    flow_run_name="raw_ingestion_flow",
)
def raw_ingestion_flow(duckdb: DuckDBProvider):
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


@flow(
    name="staging_ingestion_flow",
    flow_run_name="staging_ingestion_flow",
)
def stg_ingestion_flow(duckdb: DuckDBProvider):
    stage_table.map(
        table=STG_TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    copy_table_to_parquet.map(
        table=STG_TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    log_table_charge.map(
        table=STG_TABLES,
        duckdb=unmapped(duckdb),
    ).result()


@flow(
    name="dimension_ingestion_flow",
    flow_run_name="dimension_ingestion_flow",
)
def dim_ingestion_flow(duckdb: DuckDBProvider):
    create_table.map(
        table=DIM_TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    bootstrap_table.map(
        table=DIM_TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    upsert_table.map(
        table=DIM_TABLES,
        duckdb=unmapped(duckdb),
    ).result()

    copy_table_to_parquet.map(
        table=DIM_TABLES,
        duckdb=unmapped(duckdb),
    ).result()


@flow(
    name="fact_ingestion_flow",
    flow_run_name="fact_ingestion_flow",
)
def fct_ingestion_flow(duckdb: DuckDBProvider):
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


@flow(
    name="aggregation_ingestion_flow",
    flow_run_name="aggregation_ingestion_flow",
)
def agg_ingestion_flow(duckdb: DuckDBProvider):
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


@flow(
    name="ingestion_flow",
    flow_run_name="ingestion_flow",
)
def ingestion_flow(duckdb: DuckDBProvider):
    ddl_flow(duckdb=duckdb)

    raw_ingestion_flow(duckdb=duckdb)
    stg_ingestion_flow(duckdb=duckdb)

    dim_ingestion_flow(duckdb=duckdb)
    fct_ingestion_flow(duckdb=duckdb)
    agg_ingestion_flow(duckdb=duckdb)


if __name__ == "__main__":
    ingestion_flow(duckdb=DuckDBProvider())
