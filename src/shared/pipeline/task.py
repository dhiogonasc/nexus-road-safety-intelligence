"""src/shared/pipeline/task.py"""

from typing import Callable, Optional
from prefect import task
from config import BucketSettings
from src.shared.db.operation import (
    create_bucket_secret,
    create_schema,
)


@task(
    name="Create Schema",
    task_run_name="task_create_schema: {schema}",
)
def task_create_schema(
    conn_fn: Callable,
    schema: str,
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
    name="Create Table",
    task_run_name="task_create_table",
)
def task_create_table(
    conn_fn: Callable,
    create_table_fn: Callable,
) -> None:
    """Consolida a criação de tabelas na entidade de persistencia dedicada"""
    with conn_fn() as conn:
        create_table_fn(conn=conn)


@task(
    name="Open Bucket Operation",
    task_run_name="task_open_bucket_operation",
)
def task_open_bucket_operation(
    conn_fn: Callable,
    bucket_operation_fn: Callable,
    settings: BucketSettings,
    secret_label: str,
) -> None:
    """Consolida a abertura e execucao de operacaoes em bucket"""
    with conn_fn() as conn:
        create_bucket_secret(
            conn=conn,
            settings=settings,
            label=secret_label,
        )
        bucket_operation_fn(
            conn=conn,
            settings=settings,
        )
