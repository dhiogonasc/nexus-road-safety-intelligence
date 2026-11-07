from prefect import flow, unmapped

from src.persistence.database.provider import DuckDBProvider
from src.pipeline.acidentes.temp.task.ddl.schema.operation import create_schema
from src.pipeline.acidentes.temp.task.ddl.schema.constants.summary import SCHEMAS


@flow(
    name="schema_ddl_flow",
    flow_run_name="schema_ddl_flow",
)
def schema_ddl_flow(duckdb: DuckDBProvider):
    futures = create_schema.map(
        schema_name=SCHEMAS,
        duckdb=unmapped(duckdb),
    )
    for future in futures:
        future.result()


if __name__ == "__main__":
    schema_ddl_flow(duckdb=DuckDBProvider())
