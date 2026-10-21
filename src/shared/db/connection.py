"""src/shared/db/connection.py"""

from contextlib import contextmanager
from typing import Callable, Generator, Optional
import duckdb


@contextmanager
def create_connection(
    database: str,
    load_extensions_fn: Optional[Callable[[duckdb.DuckDBPyConnection], None]] = None,
    attach_connections_fn: Optional[Callable[[duckdb.DuckDBPyConnection], None]] = None,
) -> Generator[duckdb.DuckDBPyConnection, None, None]:
    """Gerencia a criacao de conexoes com entidades de persistencia (duckdb)"""
    conn = duckdb.connect(database)
    try:
        if load_extensions_fn:
            load_extensions_fn(conn=conn)

        if attach_connections_fn:
            attach_connections_fn(conn=conn)

        conn.execute("SET preserve_insertion_order = false;")
        conn.execute("SET threads = 2;")

        yield conn
    finally:
        conn.close()
