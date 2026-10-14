from prefect import flow
from functools import partial

from src.pipeline.index import PIPELINE_CONFIG
from src.pipeline.bronze.extract import create_stage_table_from_csv
from src.shared.pipeline.task import (
    task_create_schema,
    task_create_table_from_fn,
)
from src.shared.system.cmd import run_flow


@flow(name="Bronze")
def flow_bronze(
    database: str,
    schema: str,
) -> None:
    pipeline_schema = PIPELINE_CONFIG[schema]
    bronze_tables = pipeline_schema["bronze"]

    schema_future = task_create_schema.submit(
        database=database,
        schema=schema,
    )
    schema_future.result()

    table_futures = []
    for table, data_path in bronze_tables.items():
        future = task_create_table_from_fn.submit(
            database=database,
            create_table_fn=partial(
                create_stage_table_from_csv,
                schema=schema,
                table=table,
                csv_path=data_path,
            ),
            wait_for=schema_future,
        )
        table_futures.append(future)

    for future in table_futures:
        future.result()


if __name__ == "__main__":
    run_flow(
        flow_factory=flow_bronze,
    )
