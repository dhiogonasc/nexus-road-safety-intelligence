from prefect import flow

from src.pipeline.index import PIPELINE_CONFIG
from src.shared.pipeline.task import task_create_schema, task_create_table_from_fn
from src.shared.system.cmd import run_flow


@flow(name="Silver", flow_run_name="flow_silver: {domain}")
def flow_silver(database: str, domain: str) -> None:
    """Orquestra o processamento silver para um dominio e banco duckdb dedicado"""

    pipeline_domain = PIPELINE_CONFIG[domain]
    pipeline_stage = "silver"
    silver_tables = pipeline_domain[pipeline_stage]

    schema_future = task_create_schema.submit(
        database=database,
        schema_name=pipeline_stage,
    )
    schema_future.result()

    table_futures = {}
    wait_tasks = [schema_future]
    for table, config in silver_tables.items():
        create_table_fn = config["fn"]
        depends_on = config.get("depends_on", [])

        wait_tasks = [schema_future]
        for dep in depends_on:
            if dep in table_futures:
                wait_tasks.append(table_futures[dep])

        future = task_create_table_from_fn.submit(
            database=database,
            create_table_fn=create_table_fn,
            wait_for=wait_tasks,
        )
        table_futures[table] = future
    for future in table_futures.values():
        future.result()


if __name__ == "__main__":
    run_flow(flow_factory=flow_silver)
