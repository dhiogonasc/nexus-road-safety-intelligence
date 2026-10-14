from typing import Callable
from prefect import task
from src.shared.db.connection import create_connection
from src.shared.db.operation import create_schema


@task(
    name="Create Schema",
    task_run_name="create schema: {schema}",
)
def task_create_schema(
    database: str,
    schema: str,
) -> None:
    with create_connection(database=database) as conn:
        create_schema(
            conn=conn,
            schema=schema,
        )


@task(
    name="Create Table from Function",
    task_run_name="{create_table_fn.__name__}",
)
def task_create_table_from_fn(
    database: str,
    create_table_fn: Callable,
) -> None:
    with create_connection(database=database) as conn:
        create_table_fn(conn=conn)
