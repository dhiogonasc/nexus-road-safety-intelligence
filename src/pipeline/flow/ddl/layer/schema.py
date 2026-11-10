from prefect import flow, unmapped

from src.pipeline.model import SCHEMAS
from src.pipeline.task.ddl import create_schema
from src.persistence.database.provider import DuckDBProvider



@flow(
    name="schema_ddl_flow",
    flow_run_name="schema_ddl_flow",
)
def ddl_flow(duckdb: DuckDBProvider):
    create_schema.map(
        schema_name=SCHEMAS,
        duckdb=unmapped(duckdb),
    ).result()


if __name__ == "__main__":
    ddl_flow(duckdb=DuckDBProvider())
