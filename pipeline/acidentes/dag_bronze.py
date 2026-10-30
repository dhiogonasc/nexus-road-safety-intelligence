from functools import partial
from pathlib import Path
import tempfile

from prefect import flow

from constants import DB_DIR
from src.persistence.database.operation import create_connection, load_extensions
from src.persistence.database.settings import settings
from src.pipeline.acidentes.bronze.operation import process_layer

CATALOG = "acidentes"
LAYER = "bronze"


@flow(
    name="Flow Bronze",
    flow_run_name="acidentes: flow_bronze",
)
def flow_bronze():
    Path(DB_DIR).mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        dir=DB_DIR,
        prefix=LAYER,
    ) as bronze_dir:
        database = settings.database(name=f"{CATALOG}_{LAYER}", db_dir=bronze_dir)

        load_extensions_fn = partial(
            load_extensions,
            extensions=[
                "httpfs",
                "parquet",
            ],
        )
        conn_fn = partial(
            create_connection,
            database=database,
            load_extensions_fn=load_extensions_fn,
        )

        process_layer(conn_fn=conn_fn)


if __name__ == "__main__":
    flow_bronze()
