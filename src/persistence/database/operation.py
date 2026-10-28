"""src/shared/db/operation.py"""

from contextlib import contextmanager
from pathlib import Path
from typing import (
    Callable,
    Dict,
    List,
    Generator,
    Literal,
    Optional,
)

import duckdb


@contextmanager
def create_connection(
    database: str,
    max_memory: str = "4GB",
    enable_object_cache: str = "false",
    load_extensions_fn: Optional[Callable[[duckdb.DuckDBPyConnection], None]] = None,
    attach_connections_fn: Optional[Callable[[duckdb.DuckDBPyConnection], None]] = None,
) -> Generator[duckdb.DuckDBPyConnection, None, None]:
    """Gerencia a criacao de conexoes com entidades de persistencia (duckdb)"""
    Path(database).parent.mkdir(parents=True, exist_ok=True)
    
    conn = duckdb.connect(
        database=database,
        config={
            "max_memory": max_memory,
            "enable_object_cache": enable_object_cache,
        },
    )
    try:
        if load_extensions_fn:
            load_extensions_fn(conn=conn)
        if attach_connections_fn:
            attach_connections_fn(conn=conn)
        yield conn
    finally:
        conn.close()


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
    return conn.execute(query=query)


def attach_connections(
    conn: duckdb.DuckDBPyConnection,
    connections: List[Dict[str, str]],
) -> None:
    """Abstrai a conexao de bases para duckdb"""
    query = "\n".join(
        [
            f"ATTACH '{connection.string}' AS {connection.alias} {connection.option};"
            for connection in connections
        ]
    )
    try:
        conn.execute(query=query)
    except duckdb.BinderException:
        pass


def load_extensions(
    conn: duckdb.DuckDBPyConnection,
    extensions: List[str],
) -> None:
    """Abstrai o carregamento de extensoes para duckdb"""
    for extension in extensions:

        try:
            query = f"LOAD {extension};"
            conn.execute(query=query)

        except duckdb.BinderException:
            query = f"INSTALL {extension};\n LOAD {extension};"
            conn.execute(query=query)
