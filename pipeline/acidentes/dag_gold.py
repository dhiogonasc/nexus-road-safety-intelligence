from functools import partial
from pathlib import Path
import tempfile

from prefect import flow

from constants import DB_DIR
from src.persistence.database.operation import create_connection, load_extensions
from src.persistence.database.settings import settings
from src.pipeline.acidentes.gold.operation import process_layer

CATALOG = "acidentes"
LAYER = "gold"


@flow(
    name="Flow Gold",
    flow_run_name="acidentes: flow_gold",
)
def flow_gold():
    Path(DB_DIR).mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        dir=DB_DIR,
        prefix=LAYER,
    ) as gold_dir:
        database = settings.database(name=f"{CATALOG}_{LAYER}", db_dir=gold_dir)

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
    flow_gold()
