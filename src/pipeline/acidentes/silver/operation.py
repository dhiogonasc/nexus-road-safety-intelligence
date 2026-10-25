"""src/pipeline/silver/acidentes/transform.py"""

import duckdb

from settings import BucketSettings
from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)

def fetch_last_charged(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
) -> None:
    """Delega a execucao do script fetch_last_charged"""
    execute_query(
        conn=conn,
        query_key="fetch_last_charged",
        query_dict=QUERIES,
        settings=settings,
    )


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

def _fetch_last_charged_ufs(
    conn: duckdb.DuckDBPyConnection,
):
    """Delega a execucao do script fetch_last_charged_ufs"""
    return execute_query(
        conn=conn,
        query_key="fetch_last_charged_ufs",
        query_dict=QUERIES,
    )

def upsert_acidentes_fato_ocorrencia_per_uf(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
) -> None:
    """Delega a execucao do script upsert_acidentes_fato_ocorrencia_per_uf"""

    last_charged_ufs = [row[0] for row in _fetch_last_charged_ufs(conn=conn).fetchall()]

    for uf in last_charged_ufs:
        execute_query(
            conn=conn,
            query_key="upsert_acidentes_fato_ocorrencia_per_uf",
            query_dict=QUERIES,
            settings=settings,
            uf=uf,
        )

