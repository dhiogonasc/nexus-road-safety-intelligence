from functools import partial
from typing import Callable, ContextManager, List

import duckdb
from prefect import flow

from src.persistence.database.settings import (
    settings_temp,
    settings_main,
)
from src.persistence.database.operation import (
    attach_connections,
    create_connection,
)


from src.pipeline.acidentes.temp.ddl.operation import create_schema
from src.pipeline.acidentes.main.ddl.table.dimension.operation import (
    create_table as create_dim_tables,
    DIM_TABLES,
)
from src.pipeline.acidentes.main.ddl.table.fact.operation import (
    create_table as create_ft_tables,
    FT_TABLES,
)
from src.pipeline.acidentes.main.ddl.table.aggregation.operation import (
    create_table as create_agg_tables,
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
    schemas: List[str],
):
    futures = create_schema.map(
        conn_fn=conn_fn,
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
):
    futures = create_dim_tables.map(
        conn_fn=conn_fn,
        table_name=DIM_TABLES,
    )

    for future in futures:
        future.result()


@flow(
    name="fact_ddl_flow",
    flow_run_name="fact_ddl_flow",
)
def fact_ddl_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
):
    futures = create_ft_tables.map(
        conn_fn=conn_fn,
        table_name=FT_TABLES,
    )

    for future in futures:
        future.result()


@flow(
    name="aggregation_ddl_flow",
    flow_run_name="aggregation_ddl_flow",
)
def aggregation_ddl_flow(
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
):
    futures = create_agg_tables.map(
        conn_fn=conn_fn,
        table_name=AGG_TABLES,
    )

    for future in futures:
        future.result()


@flow(
    name="table_ddl_flow",
    flow_run_name="table_ddl_flow",
)
def ddl_flow(conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]]):
    schema_ddl_flow(
        conn_fn=conn_fn,
        schemas=SCHEMAS,
    )

    dimension_ddl_flow(conn_fn=conn_fn)
    fact_ddl_flow(conn_fn=conn_fn)
    aggregation_ddl_flow(conn_fn=conn_fn)


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

    ddl_flow(conn_fn=conn_fn)
