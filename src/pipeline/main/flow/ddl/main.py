from prefect import flow

from src.persistence.database.settings import settings
from src.persistence.database.connector import DuckDBConnector
from src.persistence.database.provider import DuckDBProvider
from .layer import schema, table


@flow(
    name="ddl_flow",
    flow_run_name="ddl_flow",
)
def ddl_flow(
    catalog_name: str,
    duckdb: DuckDBProvider,
):
    schema.ddl_flow(
        catalog_name=catalog_name,
        duckdb=duckdb,
    )
    table.ddl_flow(
        catalog_name=catalog_name,
        duckdb=duckdb,
    )


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
