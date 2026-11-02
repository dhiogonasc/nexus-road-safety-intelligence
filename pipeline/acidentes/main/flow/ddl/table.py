from functools import partial
from typing import Callable, ContextManager, Dict, List

import duckdb
from prefect import flow, task

from src.persistence.database.settings import (
    settings_main,
    settings_temp,
)
from src.persistence.database.operation import (
    load_extensions,
    attach_connections,
    create_connection,
)
from src.pipeline.acidentes.main.task.ddl.table.constants.name import (
    FACT_TABLES,
    DIMENSION_TABLES,
    AGGREGATION_TABLES,
)
from src.pipeline.acidentes.main.task.ddl.table.operation import create_table


@task(
    name="table_ddl_task_factory",
    task_run_name="table_ddl_task_factory",
)
def create_table_ddl_task_factory(
    table_names: List[str],
    catalog_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
):
    futures = create_table.map(
        table_name=table_names,
        catalog_name=catalog_name,
        conn_fn=conn_fn,
    )
    for future in futures:
        future.result()


@flow(
    name="table_ddl_flow",
    flow_run_name="table_ddl_flow",
)
def table_ddl_flow(
    catalog_name: str,
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
):
    futures = []

    dimension_future = create_table_ddl_task_factory.submit(
        table_names=DIMENSION_TABLES,
        catalog_name=catalog_name,
        conn_fn=conn_fn,
        wait_for=[],
    )

    aggregation_future = create_table_ddl_task_factory.submit(
        table_names=AGGREGATION_TABLES,
        catalog_name=catalog_name,
        conn_fn=conn_fn,
        wait_for=[],
    )
    futures.append(aggregation_future)

    fact_future = create_table_ddl_task_factory.submit(
        table_names=FACT_TABLES,
        catalog_name=catalog_name,
        conn_fn=conn_fn,
        wait_for=[dimension_future],
    )
    futures.append(fact_future)

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
        database=settings_temp.database(
            name="acidentes",
            db_dir="acidentes",
        ),
    )
    table_ddl_flow(
        conn_fn=conn_fn,
        catalog_name=settings_main.conn_alias,
    )
