from functools import partial
from typing import Callable, ContextManager, List

import duckdb
from prefect import flow

from src.persistence.database.settings import settings_main
from persistence.database.provider import (
    load_extensions,
    attach_connections,
    create_connection,
)
from src.pipeline.acidentes.main.task.ddl.schema.operation import create_schema
from src.pipeline.acidentes.main.task.ddl.schema.constants.name import SCHEMAS


@flow(
    name="schema_ddl_flow",
    flow_run_name="schema_ddl_flow",
)
def schema_ddl_flow(
    catalog_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
):
    futures = create_schema.map(
        schema_name=SCHEMAS,
        catalog_name=catalog_name,
        conn_fn=conn_fn,
    )
    for future in futures:
        future.result()


if __name__ == "__main__":
    load_extensions_fn = partial(
        load_extensions,
        extensions=["postgres"],
    )
    attach_connections_fn = partial(
        attach_connections,
        connections=[settings_main.attach_config],
    )
    conn_fn = partial(
        create_connection,
        load_extensions_fn=load_extensions_fn,
        attach_connections_fn=attach_connections_fn,
    )
    schema_ddl_flow(
        conn_fn=conn_fn,
        catalog_name=settings_main.conn_alias,
    )
