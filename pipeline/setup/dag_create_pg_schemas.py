"""pipeline/stage/dag_setup.py"""

from functools import partial
from prefect import flow

from settings import (
    duckdb_settings,
    postgres_settings,
)
from src.shared.system.cmd import declare_domain
from src.shared.pipeline.task import task_create_schema
from src.shared.db.connection import create_connection
from src.shared.db.operation import (
    load_extensions,
    attach_connections,
)


@flow(
    name="Setup",
    flow_run_name="flow_create_pg_schemas",
)
def flow_create_pg_schemas(database: str):
    """Orquestra a configuracao inicial da entidade de persistencia de agreagacoes"""

    load_postgres_extension = partial(
        load_extensions,
        extensions=duckdb_settings.EXTENSIONS,
    )
    attach_postgres = partial(
        attach_connections,
        connections=[
            {
                "conn_string": postgres_settings.postgres_conn_string,
                "conn_alias": postgres_settings.DB_NAME,
                "conn_option": "(TYPE POSTGRES)",
            }
        ],
    )
    pg_conn_fn = partial(
        create_connection,
        database=database,
        load_extensions_fn=load_postgres_extension,
        attach_connections_fn=attach_postgres,
    )
    task_create_schema(
        catalog=postgres_settings.DB_NAME,
        schema="analytics",
        conn_fn=pg_conn_fn,
    )


if __name__ == "__main__":
    args = declare_domain()

    DOMAIN = args.domain
    DATABASE = duckdb_settings.get_database_path(domain=DOMAIN)

    flow_create_pg_schemas(database=DATABASE)
