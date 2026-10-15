from prefect import flow
from src.pipeline.index import PIPELINE_CONFIG
from src.shared.pipeline.task import run_schema_pipeline
from pipeline.stage.dag_setup import flow_setup
from config import settings


@flow(name="Main")
def flow_main(database: str) -> None:
    flow_setup(database=database)

    schemas = list(PIPELINE_CONFIG.keys())

    for schema in schemas:
        run_schema_pipeline(
            database=database,
            schema_name=schema,
        )
        run_schema_pipeline.result()


if __name__ == "__main__":
    flow_main(settings.DUCKDB_PATH)
