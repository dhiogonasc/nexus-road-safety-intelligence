from functools import partial

from prefect import flow

from config import settings
from src.shared.system.cmd import domain_arg
from src.shared.db.connection import create_connection
from src.pipeline.index import PIPELINE_CONFIG
from src.shared.pipeline.task import (
    task_create_schema,
    task_create_table,
)


@flow(
    name="Silver",
    flow_run_name="flow_silver: {domain}",
)
def flow_silver(
    database: str,
    domain: str,
) -> None:
    """Orquestra o processamento silver para um dominio e banco duckdb dedicado"""

    pipeline_domain = PIPELINE_CONFIG[domain]
    pipeline_stage = "silver"
    silver_tables = pipeline_domain[pipeline_stage]

    duckdb_conn_fn = partial(
        create_connection,
        database=database,
    )
    schema_future = task_create_schema.submit(
        conn_fn=duckdb_conn_fn,
        schema=pipeline_stage,
    )

    table_futures = {}
    wait_tasks = [schema_future]
    for table, config in silver_tables.items():
        create_table_fn = config["fn"]
        depends_on = config.get("depends_on", [])

        wait_tasks = [schema_future]
        for dep in depends_on:
            if dep in table_futures:
                wait_tasks.append(table_futures[dep])

        future = task_create_table.submit(
            conn_fn=duckdb_conn_fn,
            create_table_fn=create_table_fn,
            wait_for=wait_tasks,
        )
        table_futures[table] = future
    for future in table_futures.values():
        future.result()


if __name__ == "__main__":
    args = domain_arg()

    DOMAIN = args.domain
    DATABASE = settings.domain_db_path(domain=DOMAIN)

    flow_silver(
        database=DATABASE,
        domain=DOMAIN,
    )
