from prefect import flow, settings
from functools import partial

from src.pipeline.index import PIPELINE_CONFIG
from src.pipeline.bronze.extract import create_stage_table_from_csv
from src.shared.pipeline.task import (
    task_create_schema,
    task_create_table_from_fn,
)
from src.shared.system.cmd import run_flow


def create_stage_table(table: str, data_path):
    """Cria uma função parcialmente aplicada para a extração da tabela."""

    fn = partial(
        create_stage_table_from_csv,
        table=table,
        csv_path=data_path,
    )
    fn.__name__ = f"create_stage_{table}"
    return fn


@flow(name="Bronze", flow_run_name="flow_bronze: {domain}")
def flow_bronze(database: str, domain: str) -> None:
    """Orquestra o processamento bronze para um dominio e banco duckdb dedicado"""

    pipeline_domain = PIPELINE_CONFIG[domain]
    pipeline_stage = "bronze"
    bronze_tables = pipeline_domain[pipeline_stage]

    schema_future = task_create_schema.submit(
        database=database,
        schema_name=pipeline_stage,
    )
    schema_future.result()

    table_futures = []
    for table, data_path in bronze_tables.items():

        create_table_fn = create_stage_table(
            table=table,
            data_path=data_path,
        )

        future = task_create_table_from_fn.submit(
            database=database,
            create_table_fn=create_table_fn,
            wait_for=[schema_future],
        )
        table_futures.append(future)

    for future in table_futures:
        future.result()


if __name__ == "__main__":
    run_flow(flow_factory=flow_bronze)
