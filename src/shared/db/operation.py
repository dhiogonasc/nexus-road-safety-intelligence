"""src/shared/db/operation.py"""

from typing import Optional
import duckdb

from config import BucketSettings
from src.shared.model.table import Table
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def execute_query(
    conn: duckdb.DuckDBPyConnection,
    query_dict: dict[str, str],
    query_key: str,
    **kwargs,
) -> duckdb.DuckDBPyRelation:
    """Abstrai a execucao de scripts sql para duckdb"""
    sql = query_dict[query_key]
    query = sql.format(**kwargs)
    print(query)
    return conn.execute(query)


def load_extensions(
    conn: duckdb.DuckDBPyConnection,
    extensions: str | list[str],
) -> None:
    """Abstrai a instalacao de extensoes para duckdb"""
    if isinstance(extensions, str):
        extensions = [extensions]

    for extension in extensions:
        execute_query(
            conn=conn,
            query_key="load_extension",
            query_dict=QUERIES,
            extension=extension,
        )


def attach_connections(
    conn: duckdb.DuckDBPyConnection,
    connections: list[dict[str, str]],
) -> None:
    """Abstrai a conexao de bases para duckdb"""
    for config in connections:
        conn_string = config["conn_string"]
        conn_alias = config["conn_alias"]
        conn_option = config.get("conn_option", "")

        execute_query(
            conn=conn,
            query_key="attach_connection",
            query_dict=QUERIES,
            conn_string=conn_string,
            conn_alias=conn_alias,
            conn_option=conn_option,
        )


def create_schema(
    conn: duckdb.DuckDBPyConnection,
    schema: str,
    catalog: Optional[str] = None,
) -> None:
    """Abstrai a criacao de schemas para duckdb"""
    sch = f'"{catalog}"."{schema}"' if catalog else f'"{schema}"'
    execute_query(
        conn=conn,
        query_key="create_schema",
        query_dict=QUERIES,
        schema=sch,
    )


def create_table(
    conn: duckdb.DuckDBPyConnection,
    table: Table,
) -> None:
    """Abstrai a criação de tabelas"""
    execute_query(
        conn=conn,
        query_key="create_table",
        query_dict=QUERIES,
        table=table,
    )


def create_bucket_secret(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
    label: str,
) -> None:
    """Abstrai a atualização de tabelas por logs parquet"""
    execute_query(
        conn=conn,
        query_key="create_bucket_secret",
        query_dict=QUERIES,
        settings=settings,
        label=label,
    )


def bootstrap_table(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
    domain: str,
    table: Table,
) -> None:
    """Abstrai a atualização de tabelas por logs parquet"""
    try:
        execute_query(
            conn=conn,
            query_key="bootstrap_table",
            query_dict=QUERIES,
            settings=settings,
            domain=domain,
            table=table,
        )
    except duckdb.IOException:
        pass


def copy_table_to_parquet(
    conn: duckdb.DuckDBPyConnection,
    settings: BucketSettings,
    domain: str,
    table: Table,
) -> None:
    """Abstrai a atualização de logs parquet por tabela"""
    execute_query(
        conn=conn,
        query_key="copy_table_to_parquet",
        query_dict=QUERIES,
        settings=settings,
        domain=domain,
        table=table,
    )
