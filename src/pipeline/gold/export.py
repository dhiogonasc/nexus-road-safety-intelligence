"""src/pipeline/gold/merge.py"""

import duckdb

from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def export_table(
    conn: duckdb.DuckDBPyConnection,
    source_schema: str,
    source_table: str,
    target_catalog: str,
    target_schema: str,
    target_table: str,
) -> None:
    """Consolida a exportacao das tabelas de agragacao por upsert"""
    full_source = f'"{source_schema}"."{source_table}"'
    full_target = f"{target_catalog}.{target_schema}.{target_table}"

    execute_query(
        conn=conn,
        query_key="export_table",
        query_dict=QUERIES,
        full_source=full_source,
        full_target=full_target,
    )
