from prefect import flow, task
from src.pipeline.index import PIPELINE_CONFIG
from pipeline.dag_setup import flow_setup
from pipeline.dag_bronze import flow_bronze
from pipeline.dag_silver import flow_silver
from pipeline.dag_gold import flow_gold
from config import settings


@task(
    name="Run Schema Pipeline",
    task_run_name="schema: {schema}",
)
def run_schema_pipeline(
    database: str,
    schema: str,
) -> None:
    flow_bronze(
        database=database,
        schema=schema,
    )
    flow_silver(
        database=database,
        schema=schema,
    )
    flow_gold(
        database=database,
        schema=schema,
    )


@flow(name="Main")
def flow_main(database: str) -> None:
    flow_setup(database=database)

    schemas = list(PIPELINE_CONFIG.keys())

    for schema in schemas:
        run_schema_pipeline(
            database=database,
            schema=schema,
        )
        run_schema_pipeline.result()


if __name__ == "__main__":
    flow_main(settings.DUCKDB_PATH)
