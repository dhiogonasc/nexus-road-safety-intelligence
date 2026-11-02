from functools import partial
from typing import Callable, ContextManager, List

import duckdb
from prefect import flow

from src.persistence.database.settings import settings_temp
from src.persistence.database.operation import create_connection
from src.pipeline.acidentes.temp.task.ddl.schema.operation import create_schema
from src.pipeline.acidentes.temp.task.ddl.schema.constants.name import SCHEMAS


@flow(
    name="ddl_flow",
    flow_run_name="ddl_flow: {schemas}",
)
def schema_ddl_flow(
    schemas: List[str],
    conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
):
    futures = create_schema.map(
        schema_name=schemas,
        conn_fn=conn_fn,
    )
    for future in futures:
        future.result()


if __name__ == "__main__":
    conn_fn = partial(
        create_connection,
        database=settings_temp.database(
            name="acidentes",
            db_dir="acidentes",
        ),
    )
    schema_ddl_flow(
        conn_fn=conn_fn,
        schemas=SCHEMAS,
    )
