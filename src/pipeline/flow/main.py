from tempfile import TemporaryDirectory

from prefect import flow

from src.persistence.database.connector import DuckDBConnector
from src.persistence.database.settings import DuckDBSettings
from src.persistence.database.provider import DuckDBProvider
from .ddl.main import ddl_flow
from .ingestion.main import ingestion_flow


@flow(
    name="ingestion_flow",
    flow_run_name="ingestion_flow",
)
def main_flow(duckdb: DuckDBProvider):
    ddl_flow(duckdb=duckdb)
    ingestion_flow(duckdb=duckdb)


if __name__ == "__main__":
    with TemporaryDirectory() as temp_dir:
        settings = DuckDBSettings(directory=temp_dir)
        connector = DuckDBConnector(settings=settings)
        provider = DuckDBProvider(connector=connector)

        main_flow(duckdb=provider)
