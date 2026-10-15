from prefect import flow
from src.shared.system.cmd import run_flow
from src.shared.pipeline.task import run_schema_pipeline
from pipeline.stage.dag_setup import flow_setup


@flow(name="Main")
def flow_schema(
    database: str,
    schema: str,
) -> None:
    flow_setup(database=database)

    run_schema_pipeline(
        database=database,
        schema_name=schema,
    )
    run_schema_pipeline.result()


if __name__ == "__main__":
    run_flow(
        flow_factory=flow_schema,
    )
