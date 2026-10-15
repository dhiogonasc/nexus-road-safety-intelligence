from prefect import flow, task
from functools import partial

from config import settings
from src.shared.db.connection import create_connection
from src.shared.db.operation import (
    create_schema,
    load_extensions,
    attach_connections,
)
from src.pipeline.setup.extension import install_extension


@task(
    name="Install Extension",
    task_run_name="install extension: {extension}",
)
def task_install_extension(
    database: str,
    extension: str,
) -> None:
    with create_connection(database=database) as conn:
        install_extension(
            conn=conn,
            extension=extension,
        )


@task(
    name="Create Schema",
    task_run_name="create schema: analytics",
)
def task_create_analytics_schema(database: str) -> None:
    load_postgres_extension = partial(
        load_extensions,
        extensions=["postgres"],
    )
    attach_postgres = partial(
        attach_connections,
        connections=[
            {
                "conn_string": settings.postgres_conn_string,
                "conn_alias": "pg_rsi_pei6",
                "conn_option": "(TYPE POSTGRES)",
            }
        ],
    )

    with create_connection(
        database=database,
        load_extensions_fn=load_postgres_extension,
        attach_connections_fn=attach_postgres,
    ) as conn:
        create_schema(
            conn=conn,
            schema="analytics",
            catalog="pg_rsi_pei6",
        )


@flow(name="Setup")
def flow_setup(database: str):

    for extension in settings.DUCKDB_EXTENSIONS:
        task_install_extension.submit(
            database=database,
            extension=extension,
        )

    task_create_analytics_schema(database=database)


if __name__ == "__main__":
    flow_setup(database=settings.DUCKDB_PATH)
