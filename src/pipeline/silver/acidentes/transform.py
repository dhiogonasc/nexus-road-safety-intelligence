"""src/pipeline/silver/acidentes/transform.py"""

import duckdb

from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def create_acidentes_dim_tempo(conn: duckdb.DuckDBPyConnection) -> None:
    """Delega a execucao do script create_acidentes_dim_tempo.sql"""
    execute_query(
        conn=conn,
        query_key="create_acidentes_dim_tempo",
        query_dict=QUERIES,
    )


def create_acidentes_dim_coordenada(conn: duckdb.DuckDBPyConnection) -> None:
    """Delega a execucao do script create_acidentes_dim_coordenada.sql"""
    execute_query(
        conn=conn,
        query_key="create_acidentes_dim_coordenada",
        query_dict=QUERIES,
    )


def create_acidentes_dim_localizacao(conn: duckdb.DuckDBPyConnection) -> None:
    """Delega a execucao do script create_acidentes_dim_localizacao.sql"""
    execute_query(
        conn=conn,
        query_key="create_acidentes_dim_localizacao",
        query_dict=QUERIES,
    )


def create_acidentes_dim_pista(conn: duckdb.DuckDBPyConnection) -> None:
    """Delega a execucao do script create_acidentes_dim_pista.sql"""
    execute_query(
        conn=conn,
        query_key="create_acidentes_dim_pista",
        query_dict=QUERIES,
    )


def create_acidentes_dim_causa(conn: duckdb.DuckDBPyConnection) -> None:
    """Delega a execucao do script create_acidentes_dim_causa.sql"""
    execute_query(
        conn=conn,
        query_key="create_acidentes_dim_causa",
        query_dict=QUERIES,
    )


def create_acidentes_dim_tipo(conn: duckdb.DuckDBPyConnection) -> None:
    """Delega a execucao do script create_acidentes_dim_tipo.sql"""
    execute_query(
        conn=conn,
        query_key="create_acidentes_dim_tipo",
        query_dict=QUERIES,
    )


def create_acidentes_dim_classificacao(conn: duckdb.DuckDBPyConnection) -> None:
    """Delega a execucao do script create_acidentes_dim_classificacao.sql"""
    execute_query(
        conn=conn,
        query_key="create_acidentes_dim_classificacao",
        query_dict=QUERIES,
    )


def create_acidentes_fato_ocorrencia(conn: duckdb.DuckDBPyConnection) -> None:
    """Delega a execucao do script create_acidentes_fato_ocorrencia.sql"""
    execute_query(
        conn=conn,
        query_key="create_acidentes_fato_ocorrencia",
        query_dict=QUERIES,
    )
