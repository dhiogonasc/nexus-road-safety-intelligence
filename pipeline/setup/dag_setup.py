"""pipeline/setup/dag_install_extensions.py"""

from functools import partial
from typing import Callable, List
from prefect import flow, task

from src.persistence.database import DuckDBSettings
from src.persistence.database.operation import (
    create_connection,
    install_extensions,
)


@task(
    name="Install Extension",
    task_run_name="task_install_extensions: {extensions}",
)
def task_install_extensions(
    conn_fn: Callable,
    extensions: List[str],
) -> None:
    """Consolida a instalação de extensões"""
    with conn_fn() as conn:
        install_extensions(
            conn=conn,
            extensions=extensions,
        )


@flow(
    name="Setup",
    flow_run_name="flow_setup: {catalog}",
)
def flow_setup(
    catalog: str,
    settings: DuckDBSettings,
):
    """Orquestra a instalação de extensões"""
    database = settings.database(catalog=catalog)
    extensions = settings.EXTENSIONS

    conn_fn = partial(
        create_connection,
        database=database,
    )

    future = task_install_extensions.submit(
        conn_fn=conn_fn,
        extensions=extensions,
    )
    future.result()
