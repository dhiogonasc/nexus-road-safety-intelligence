"""pipeline/dag_main.py"""

from pathlib import Path
from prefect import flow, task

from pipeline.exportion.dag_exportation import flow_exportation
from settings import duckdb_settings
from pipeline.setup.dag_install_extensions import flow_install_extensions
from pipeline.medallion.dag_bronze import flow_bronze
from pipeline.medallion.dag_silver import flow_silver
from pipeline.medallion.dag_gold import flow_gold
from src.shared.system.cmd import declare_domain
from src.shared.system.file import delete_file


@task(
    name="Clean Persistence",
    task_run_name="task_clean_persistence: {filename}",
)
def task_clean_persistence(
    dir_path: str | Path,
    filename: str,
):
    delete_file(
        dir_path=dir_path,
        filename=filename,
    )


@flow(
    name="Setup",
    flow_run_name="flow_setup",
)
def flow_setup(database: str):
    """Orquestra a configuracao inicial das entidades de persistencia"""

    flow_install_extensions(database=database)


@flow(
    name="Main",
    flow_run_name="flow_main: {domain}",
)
def flow_main(
    database: str,
    domain: str,
) -> None:
    """Orquestra a pipeline ETL de um dominio para uma entidade de persistencia dedicada."""

    flow_setup(database=database)

    flow_bronze(
        database=database,
        domain=domain,
    )
    flow_silver(
        database=database,
        domain=domain,
    )
    flow_gold(
        database=database,
        domain=domain,
    )

    flow_exportation(
        database=database,
        domain=domain,
    )

    task_clean_persistence(
        dir_path=duckdb_settings.DB_DIR,
        filename=f"{domain}.db",
    )


if __name__ == "__main__":
    arg = declare_domain()
    DOMAIN = arg.domain
    DATABASE = duckdb_settings.get_database_path(domain=DOMAIN)
    flow_main(database=DATABASE, domain=DOMAIN)
