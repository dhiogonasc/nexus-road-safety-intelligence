"""src/shared/pipeline/task.py"""

from typing import Callable, Optional
from prefect import task
from src.shared.db.connection import create_connection
from src.shared.db.operation import create_schema


@task(
    name="Create Schema",
    task_run_name="task_create_schema: {schema}",
)
def task_create_schema(
    schema: str,
    conn_fn: Callable,
    catalog: Optional[str] = None,
) -> None:
    """Consolida a criacao de schema para um dominio na entidade de persistencia dedicada"""
    with conn_fn() as conn:
        create_schema(
            conn=conn,
            schema=schema,
            catalog=catalog,
        )


@task(
    name="Create Table from Function",
    task_run_name="task_create_table_from_fn: {create_table_fn.__name__}",
)
def task_create_table_from_fn(
    database: str,
    create_table_fn: Callable,
) -> None:
    """Consolida a criação de tabelas na entidade de persistencia dedicada"""
    with create_connection(database=database) as conn:
        create_table_fn(conn=conn)
