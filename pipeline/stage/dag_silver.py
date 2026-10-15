from prefect import flow

from src.pipeline.index import PIPELINE_CONFIG
from src.shared.pipeline.task import task_create_table_from_fn
from src.shared.system.cmd import run_flow


@flow(name="Silver")
def flow_silver(
    database: str,
    schema: str,
) -> None:
    pipeline_schema = PIPELINE_CONFIG[schema]
    silver_tables = pipeline_schema["silver"]

    table_futures = {}
    for table_name, table_config in silver_tables.items():
        create_fn = table_config["fn"]
        depends_on = table_config.get("depends_on", [])

        wait_tasks = [table_futures[dep] for dep in depends_on if dep in table_futures]

        future = task_create_table_from_fn.submit(
            database=database,
            create_table_fn=create_fn,
            wait_for=wait_tasks,
        )

        table_futures[table_name] = future

    for future in table_futures.values():
        future.result()


if __name__ == "__main__":
    run_flow(
        flow_factory=flow_silver,
    )
