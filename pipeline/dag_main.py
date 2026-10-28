from prefect import flow

from .setup.dag_setup import flow_setup

from src.persistence.database import duckdb_settings, DuckDBSettings
from src.shared.system.cmd import declare_catalog


@flow(
    name="Main",
    flow_run_name="flow_main: {catalog}",
)
def flow_main(
    catalog: str,
    settings: DuckDBSettings,
) -> None:
    flow_setup(
        catalog=catalog,
        settings=settings,
    )


if __name__ == "__main__":
    arg = declare_catalog()
    CATALOG = arg.catalog
    flow_main(
        catalog=CATALOG,
        settings=duckdb_settings,
    )
