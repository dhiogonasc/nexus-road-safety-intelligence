"""pipeline/dag_main.py"""

from pathlib import Path
from prefect import flow, task

from config import settings
from constants import DATABASE_DIR
from pipeline.setup.dag_create_pg_schemas import flow_create_pg_schemas
from pipeline.setup.dag_install_extensions import flow_install_extensions
from pipeline.stage.dag_bronze import flow_bronze
from pipeline.stage.dag_silver import flow_silver
from pipeline.stage.dag_gold import flow_gold
from src.shared.system.file import delete_file
from src.shared.system.cmd import declare_domain

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
    flow_create_pg_schemas(database=database)


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
    
    task_clean_persistence(
        dir_path=DATABASE_DIR, 
        filename=f"{domain}.db"
    )


if __name__ == "__main__":
    args = declare_domain()

    DOMAIN = args.domain
    DATABASE = settings.domain_db_path(domain=DOMAIN)

    flow_main(
        database=DATABASE,
        domain=DOMAIN,
    )
