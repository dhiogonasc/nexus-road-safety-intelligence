from functools import partial

from src.pipeline.acidentes.gold.operation import process_layer
from src.persistence.database import duckdb_settings
from src.persistence.database.operation import create_connection, load_extensions
from src.shared.system.cmd import declare_catalog


if __name__ == "__main__":
    arg = declare_catalog()

    load_extensions_fn = partial(
        load_extensions,
        extensions=[
            "httpfs",
            "parquet",
        ],
    )
    conn_fn = partial(
        create_connection,
        load_extensions_fn=load_extensions_fn,
        database=duckdb_settings.database(catalog=arg.catalog),
    )

    process_layer(conn_fn=conn_fn)
