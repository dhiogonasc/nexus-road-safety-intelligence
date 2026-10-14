import duckdb

from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def create_stage_table_from_csv(
    conn: duckdb.DuckDBPyConnection,
    schema: str,
    table: str,
    csv_path: str,
    delim: str = ";",
    encoding: str = "latin-1",
) -> None:
    execute_query(
        conn=conn,
        query_key="create_stage_table_from_csv",
        query_dict=QUERIES,
        schema=schema,
        table=table,
        csv_path=csv_path,
        delim=delim,
        encoding=encoding,
    )
