from typing import Callable
from prefect import task
from pipeline.stage.dag_bronze import flow_bronze
from pipeline.stage.dag_gold import flow_gold
from pipeline.stage.dag_silver import flow_silver
from src.shared.db.connection import create_connection
from src.shared.db.operation import create_schema


@task(
    name="Create Schema",
    task_run_name="create schema: {schema_name}",
)
def task_create_schema(
    database: str,
    schema_name: str,
) -> None:
    with create_connection(database=database) as conn:
        create_schema(
            conn=conn,
            schema=schema_name,
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


@task(
    name="Run Schema Pipeline",
    task_run_name="schema: {schema_name}",
)
def run_schema_pipeline(
    database: str,
    schema_name: str,
) -> None:
    flow_bronze(
        database=database,
        schema=schema_name,
    )
    flow_silver(
        database=database,
        schema=schema_name,
    )
    flow_gold(
        database=database,
        schema=schema_name,
    )
