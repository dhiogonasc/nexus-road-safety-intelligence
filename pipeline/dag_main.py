"""pipeline/dag_main.py"""

from prefect import flow
from pipeline.stage.dag_setup import flow_setup
from pipeline.stage.dag_bronze import flow_bronze
from pipeline.stage.dag_silver import flow_silver
from pipeline.stage.dag_gold import flow_gold
from src.shared.pipeline.run import run_flow


@flow(
    name="Main",
    flow_run_name="flow_main: {domain}",
)
def flow_main(
    database: str,
    domain: str,
) -> None:
    """Orquestra a pipeline ETL de um dominio para uma entidade de persistencia dedicada."""

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
    run_flow(flow_factory=flow_main)
