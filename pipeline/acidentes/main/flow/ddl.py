from functools import partial
from typing import Callable, ContextManager, List

import duckdb
from prefect import flow, futures

from src.persistence.database.settings import (
    settings_temp,
    settings_main,
)
from src.persistence.database.operation import (
    attach_connections,
    create_connection,
    load_extensions,
)


from src.pipeline.acidentes.main.ddl.schema.operation import create as create_schema
from src.pipeline.acidentes.main.ddl.table.dimension.operation import (
    create as create_dim_tables,
    DIM_TABLES,
)
from src.pipeline.acidentes.main.ddl.table.fact.operation import (
    create as create_ft_tables,
    FT_TABLES,
)
from src.pipeline.acidentes.main.ddl.table.aggregation.operation import (
    create as create_agg_tables,
    AGG_TABLES,
)

SCHEMAS = [
    "core",
    "analytics",
]


@flow(
    name="schema_ddl_flow",
    flow_run_name="schema_ddl_flow: {schemas}",
)
def schema_ddl_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    catalog_name: str,
    schemas: List[str],
):
    futures = create_schema.map(
        conn_fn=conn_fn,
        catalog_name=catalog_name,
        schema_name=schemas,
    )
    for future in futures:
        future.result()


@flow(
    name="dimension_ddl_flow",
    flow_run_name="dimension_ddl_flow",
)
def dimension_ddl_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    catalog_name: str,
):
    futures = create_dim_tables.map(
        conn_fn=conn_fn,
        table_name=DIM_TABLES,
        catalog_name=catalog_name,
    )

    for future in futures:
        future.result()


@flow(
    name="fact_ddl_flow",
    flow_run_name="fact_ddl_flow",
)
def fact_ddl_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    catalog_name: str,
):
    futures = create_ft_tables.map(
        conn_fn=conn_fn,
        table_name=FT_TABLES,
        catalog_name=catalog_name,
    )

    for future in futures:
        future.result()


@flow(
    name="aggregation_ddl_flow",
    flow_run_name="aggregation_ddl_flow",
)
def aggregation_ddl_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
    catalog_name: str,
):
    futures = create_agg_tables.map(
        conn_fn=conn_fn,
        table_name=AGG_TABLES,
        catalog_name=catalog_name,
    )

    for future in futures:
        future.result()


@flow(
    name="table_ddl_flow",
    flow_run_name="table_ddl_flow",
)
def ddl_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]], catalog_name: str
):
    schema_ddl_flow(
        conn_fn=conn_fn,
        catalog_name=catalog_name,
        schemas=SCHEMAS,
    )

    dimension_ddl_flow(
        conn_fn=conn_fn,
        catalog_name=catalog_name,
    )
    fact_ddl_flow(
        conn_fn=conn_fn,
        catalog_name=catalog_name,
    )
    aggregation_ddl_flow(
        conn_fn=conn_fn,
        catalog_name=catalog_name,
    )


if __name__ == "__main__":
    load_extensions_fn = partial(
        load_extensions,
        extensions=["postgres"],
    )
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
        load_extensions_fn=load_extensions_fn,
        attach_connections_fn=attach_connections_fn,
        database=settings_temp.database(
            name="acidentes",
            db_dir="acidentes",
        ),
    )

    ddl_flow(
        conn_fn=conn_fn,
        catalog_name=settings_main.DB_NAME,
    )
