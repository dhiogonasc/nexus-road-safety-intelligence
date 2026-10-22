"""src/pipeline/silver/acidentes/transform.py"""

import duckdb

from config import BucketSettings
from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def upsert_acidentes_dim_causa(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
) -> None:
    """Delega a execucao do script upsert_acidentes_dim_causa"""
    execute_query(
        conn=conn,
        query_key="upsert_acidentes_dim_causa",
        query_dict=QUERIES,
        settings=settings,
    )


def upsert_acidentes_dim_classificacao(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
) -> None:
    """Delega a execucao do script upsert_acidentes_dim_classificacao"""
    execute_query(
        conn=conn,
        query_key="upsert_acidentes_dim_classificacao",
        query_dict=QUERIES,
        settings=settings,
    )


def upsert_acidentes_dim_tipo(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
) -> None:
    """Delega a execucao do script upsert_acidentes_dim_tipo"""
    execute_query(
        conn=conn,
        query_key="upsert_acidentes_dim_tipo",
        query_dict=QUERIES,
        settings=settings,
    )


def upsert_acidentes_dim_condicao_metereologica(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
) -> None:
    """Delega a execucao do script upsert_acidentes_dim_condicao_metereologica"""
    execute_query(
        conn=conn,
        query_key="upsert_acidentes_dim_condicao_metereologica",
        query_dict=QUERIES,
        settings=settings,
    )

def upsert_acidentes_dim_coordenada(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
) -> None:
    """Delega a execucao do script upsert_acidentes_dim_coordenada"""
    execute_query(
        conn=conn,
        query_key="upsert_acidentes_dim_coordenada",
        query_dict=QUERIES,
        settings=settings,
    )

def upsert_acidentes_dim_tempo(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
) -> None:
    """Delega a execucao do script upsert_acidentes_dim_tempo"""
    execute_query(
        conn=conn,
        query_key="upsert_acidentes_dim_tempo",
        query_dict=QUERIES,
        settings=settings,
    )

def upsert_acidentes_dim_pista(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
) -> None:
    """Delega a execucao do script upsert_acidentes_dim_pista"""
    execute_query(
        conn=conn,
        query_key="upsert_acidentes_dim_pista",
        query_dict=QUERIES,
        settings=settings,
    )

def upsert_acidentes_dim_localizacao(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
) -> None:
    """Delega a execucao do script upsert_acidentes_dim_localizacao"""
    execute_query(
        conn=conn,
        query_key="upsert_acidentes_dim_localizacao",
        query_dict=QUERIES,
        settings=settings,
    )

def upsert_acidentes_fato_ocorrencia(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
) -> None:
    """Delega a execucao do script upsert_acidentes_fato_ocorrencia"""
    execute_query(
        conn=conn,
        query_key="upsert_acidentes_fato_ocorrencia",
        query_dict=QUERIES,
        settings=settings,
    )

