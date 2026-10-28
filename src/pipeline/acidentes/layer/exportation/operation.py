"""src/pipeline/gold/acidentes/load.py"""

import duckdb

from settings import BucketSettings
from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def upsert_exportation_acidentes_agg_condicoes_via(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
    catalog: str,
) -> None:
    """Delega a execucao do script upsert_exportation_acidentes_agg_condicoes_via.sql"""
    execute_query(
        conn=conn,
        query_key="upsert_exportation_acidentes_agg_condicoes_via",
        query_dict=QUERIES,
        settings=settings,
        catalog=catalog,
    )


def upsert_exportation_acidentes_agg_sazonalidade(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
    catalog: str,
) -> None:
    """Delega a execucao do script upsert_exportation_acidentes_agg_sazonalidade.sql"""
    execute_query(
        conn=conn,
        query_key="upsert_exportation_acidentes_agg_sazonalidade",
        query_dict=QUERIES,
        settings=settings,
        catalog=catalog,
    )
    
    
def upsert_exportation_acidentes_agg_trechos_criticos(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
    catalog: str,
) -> None:
    """Delega a execucao do script upsert_exportation_acidentes_agg_trechos_criticos.sql"""
    execute_query(
        conn=conn,
        query_key="upsert_exportation_acidentes_agg_trechos_criticos",
        query_dict=QUERIES,
        settings=settings,
        catalog=catalog,
    ) 