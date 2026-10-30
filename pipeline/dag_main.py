from functools import partial

from src.pipeline.acidentes.bronze.operation import process_layer as flow_bronze
from src.pipeline.acidentes.silver.operation import process_layer as flow_silver
from src.pipeline.acidentes.gold.operation import process_layer as flow_gold
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

    flow_bronze(conn_fn=conn_fn)
    flow_silver(conn_fn=conn_fn)
    flow_gold(conn_fn=conn_fn)
