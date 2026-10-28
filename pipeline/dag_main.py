from functools import partial

from src.pipeline import catalogs
from src.shared.pipeline.task import flow_process_catalog
from src.persistence.database import duckdb_settings
from src.persistence.database.operation import create_connection
from src.shared.system.cmd import declare_catalog

if __name__ == "__main__":
    arg = declare_catalog()
    CATALOG = catalogs[arg.catalog]

    conn_fn = partial(
        create_connection,
        database=duckdb_settings.database(catalog=CATALOG.label),
    )

    flow_process_catalog(
        catalog=CATALOG,
        conn_fn=conn_fn,
    )
