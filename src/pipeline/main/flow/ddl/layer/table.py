from prefect import flow, unmapped

from src.persistence.database.settings import settings
from src.persistence.database.connector import DuckDBConnector
from src.persistence.database.provider import DuckDBProvider
from src.pipeline.main.task.ddl.table.constants.name import (
    DIMENSION_TABLES,
    FACT_TABLES,
    AGGREGATION_TABLES,
)
from src.pipeline.main.task.ddl.table.operation import create_table


@flow(
    name="table_ddl_flow",
    flow_run_name="table_ddl_flow",
)
def ddl_flow(
    catalog_name: str,
    duckdb: DuckDBProvider,
):
    create_table.map(
        table=DIMENSION_TABLES,
        catalog_name=unmapped(catalog_name),
        duckdb=unmapped(duckdb),
    ).result()

    create_table.map(
        table=FACT_TABLES,
        catalog_name=unmapped(catalog_name),
        duckdb=unmapped(duckdb),
    ).result()

    create_table.map(
        table=AGGREGATION_TABLES,
        catalog_name=unmapped(catalog_name),
        duckdb=unmapped(duckdb),
    ).result()


if __name__ == "__main__":
    connector = DuckDBConnector(
        extensions=["postgres"],
        attach_configs=[settings.attach_config],
    )
    duckdb = DuckDBProvider(
        connector=connector,
    )

    ddl_flow(
        catalog_name=settings.conn_alias,
        duckdb=duckdb,
    )
