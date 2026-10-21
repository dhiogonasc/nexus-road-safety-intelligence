"""src/pipeline/silver/acidentes/transform.py"""

from typing import Callable

import duckdb

from config import BucketSettings
from src.shared.model.table import Table
from src.shared.db.operation import (
    bootstrap_table,
    copy_table_to_parquet,
    create_table,
    execute_query,
)
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def process_table(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
    domain: str,
    table: Table,
    upsert_fn: Callable,
) -> None:
    """Delega a execucao do processamento da uma tabela"""
    create_table(
        conn=conn,
        table=table,
    )
    try:
        bootstrap_table(
            conn=conn,
            domain=domain,
            table=table,
            settings=settings,
        )
    except (duckdb.IOException, duckdb.ParserException):
        pass
    upsert_fn(
        conn=conn,
        settings=settings,
    )
    copy_table_to_parquet(
        conn=conn,
        domain=domain,
        table=table,
        settings=settings,
    )


def upsert_acidentes_dim_causa(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
):
    """Delega a execucao do script upsert_acidentes_dim_causa"""
    execute_query(
        conn=conn,
        query_key="upsert_acidentes_dim_causa",
        query_dict=QUERIES,
        settings=settings,
    )

    
