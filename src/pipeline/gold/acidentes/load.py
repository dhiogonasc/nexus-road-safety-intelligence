import duckdb

from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def create_acidentes_agg_sazonalidade(conn: duckdb.DuckDBPyConnection) -> None:
    execute_query(
        conn=conn,
        query_key="create_acidentes_agg_sazonalidade",
        query_dict=QUERIES,
    )

def create_acidentes_agg_trechos_criticos(conn: duckdb.DuckDBPyConnection) -> None:
    execute_query(
        conn=conn,
        query_key="create_acidentes_agg_trechos_criticos",
        query_dict=QUERIES,
    )
    
def create_acidentes_agg_condicoes_via(conn: duckdb.DuckDBPyConnection) -> None:
    execute_query(
        conn=conn,
        query_key="create_acidentes_agg_condicoes_via",
        query_dict=QUERIES,
    )
    
def create_acidentes_agg_localidade(conn: duckdb.DuckDBPyConnection) -> None:
    execute_query(
        conn=conn,
        query_key="create_acidentes_agg_localidade",
        query_dict=QUERIES,
    )
