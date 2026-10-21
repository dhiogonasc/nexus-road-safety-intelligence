"""src/pipeline/silver/acidentes/dim_causa/transform.py"""

import duckdb

from config import BucketSettings
from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)

DIM_CAUSA_FNS = {}


def process_dim_causa(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
) -> None:
    """Delega a execucao do script create_dim_causa.sql"""

    _create_dim_causa(conn=conn)
    try:
        _bootstrap_dim_causa(
            conn=conn,
            settings=settings,
        )
    except (duckdb.IOException, duckdb.BinderException):
        pass

    _upsert_dim_causa(
        conn=conn,
        settings=settings,
    )
    _copy_dim_causa_to_parquet(
        conn=conn,
        settings=settings,
    )


def _create_dim_causa(conn: duckdb.DuckDBPyConnection) -> duckdb.DuckDBPyRelation:
    """Delega a execucao do script create_dim_causa.sql"""
    return execute_query(
        conn=conn,
        query_key="create_dim_causa",
        query_dict=QUERIES,
    )


def _upsert_dim_causa(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
) -> duckdb.DuckDBPyRelation:
    """Delega a execucao do script upsert_dim_causa.sql"""
    return execute_query(
        conn=conn,
        query_key="upsert_dim_causa",
        query_dict=QUERIES,
        settings=settings,
    )


def _bootstrap_dim_causa(
    conn: duckdb.DuckDBPyConnection, settings: BucketSettings
) -> duckdb.DuckDBPyRelation:
    """Delega a execucao do script bootstrap_dim_causa.sql"""
    return execute_query(
        conn=conn,
        query_key="bootstrap_dim_causa",
        query_dict=QUERIES,
        settings=settings,
    )


def _copy_dim_causa_to_parquet(
    conn: duckdb.DuckDBPyConnection, settings: BucketSettings
) -> duckdb.DuckDBPyRelation:
    """Delega a execucao do script copy_dim_causa_to_parquet.sql"""
    return execute_query(
        conn=conn,
        query_key="copy_dim_causa_to_parquet",
        query_dict=QUERIES,
        settings=settings,
    )
