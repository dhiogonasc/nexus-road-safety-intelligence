from prefect import flow, unmapped

from src.persistence.database.connector import DuckDBConnector
from src.persistence.database.provider import DuckDBProvider
from src.persistence.database.settings import settings
from src.pipeline.main.task.ddl.schema.operation import create_schema
from src.pipeline.main.task.ddl.schema.constants.summary import SCHEMAS


@flow(
    name="schema_ddl_flow",
    flow_run_name="schema_ddl_flow",
)
def ddl_flow(
    catalog_name: str,
    duckdb: DuckDBProvider,
):
    create_schema.map(
        schema_name=SCHEMAS,
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
