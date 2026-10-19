from prefect import flow
from config import settings
from pipeline.stage.dag_setup import flow_setup
from pipeline.stage.dag_bronze import flow_bronze
from pipeline.stage.dag_silver import flow_silver
from pipeline.stage.dag_gold import flow_gold
from src.shared.system.cmd import run_flow


@flow(name="Main")
def flow_domain(database: str, domain: str) -> None:
    """Orquestra a pipeline ETL de um dominio."""

    flow_setup(
        database=database, 
        domain=domain,
    )
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


if __name__ == "__main__":
    run_flow(flow_factory=flow_domain)
