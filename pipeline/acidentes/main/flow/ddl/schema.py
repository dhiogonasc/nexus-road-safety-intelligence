from functools import partial
from typing import Callable, ContextManager, List

import duckdb
from prefect import flow

from src.persistence.database.settings import settings_temp, settings_main
from src.persistence.database.operation import attach_connections, create_connection
from src.pipeline.acidentes.temp.ddl.operation import create_schema

SCHEMAS = [
    "core",
    "analytics",
]


@flow(
    name="ddl_flow",
    flow_run_name="ddl_flow: {schemas}",
)
def schema_ddl_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    schemas: List[str],
):
    futures = create_schema.map(
        conn_fn=conn_fn,
        schema_name=schemas,
    )
    for future in futures:
        future.result()


if __name__ == "__main__":
    attach_connections_fn = partial(
        attach_connections,
        connections=[
            {
                "string": settings_main.conn_string,
                "alias": settings_main.DB_NAME,
                "option": "(TYPE POSTGRES)",
            }
        ],
    )
    conn_fn = partial(
        create_connection,
        database=settings_temp.database(name="acidentes", db_dir="acidentes"),
    )
    schema_ddl_flow(
        conn_fn=conn_fn,
        schemas=SCHEMAS,
    )
