"""pipeline/setup/dag_install_extensions.py"""

from functools import partial
from typing import Callable
from prefect import flow, task

from settings import settings
from src.shared.system.cmd import declare_domain
from src.shared.db.connection import create_connection
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
    name="Install Extensions",
    flow_run_name="flow_install_extensions",
)
def flow_install_extensions(database: str):
    """Orquestra a configuracao inicial da entidade de persistencia local"""

    duckdb_conn_fn = partial(
        create_connection,
        database=database,
    )

    install_extension_futures = []
    for extension in settings.DUCKDB_EXTENSIONS:
        future = task_install_extension.submit(
            extension=extension,
            conn_fn=duckdb_conn_fn,
        )
        install_extension_futures.append(future)

    for future in install_extension_futures:
        future.result()


if __name__ == "__main__":
    args = declare_domain()

    DOMAIN = args.domain
    DATABASE = settings.domain_db_path(domain=DOMAIN)

    flow_install_extensions(database=DATABASE)
