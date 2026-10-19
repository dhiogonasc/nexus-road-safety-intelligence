"""pipeline/stage/dag_setup.py"""

from functools import partial
from typing import Callable
from prefect import flow, task

from config import settings
from src.shared.system.cmd import declare_domain
from src.shared.pipeline.task import task_create_schema
from src.shared.db.connection import create_connection
from src.shared.db.operation import (
    load_extensions,
    attach_connections,
)
from src.pipeline.setup.extension import install_extension


@task(
    name="Install Extension",
    task_run_name="task_install_extension: {extension}",
)
def task_install_extension(
    extension: str,
    conn_fn: Callable,
) -> None:
    """Consolida a instalação de extensões em uma base de dados"""

    with conn_fn() as conn:
        install_extension(
            conn=conn,
            extension=extension,
        )


@flow(
    name="Setup",
    flow_run_name="flow_setup",
)
def flow_setup(database: str):
    """Orquestra a configuracao inicial das entidades de persistencia"""

    duckdb_conn_fn = partial(
        create_connection,
        database=database,
    )
    for extension in settings.DUCKDB_EXTENSIONS:
        task_install_extension.submit(
            extension=extension,
            conn_fn=duckdb_conn_fn,
        )

    catalog = settings.DB_NAME
    load_postgres_extension = partial(
        load_extensions,
        extensions=["postgres"],
    )
    attach_postgres = partial(
        attach_connections,
        connections=[
            {
                "conn_string": settings.postgres_conn_string,
                "conn_alias": catalog,
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
        catalog=catalog,
        schema="analytics",
        conn_fn=pg_conn_fn,
    )


if __name__ == "__main__":
    args = declare_domain()

    DOMAIN = args.domain
    DATABASE = settings.domain_db_path(domain=DOMAIN)

    flow_setup(database=DATABASE)
