from contextlib import contextmanager
from typing import Callable, Generator, Optional
import duckdb


@contextmanager
def create_connection(
    database: str,
    load_extensions_fn: Optional[Callable[[duckdb.DuckDBPyConnection], None]] = None,
    attach_connections_fn: Optional[Callable[[duckdb.DuckDBPyConnection], None]] = None,
) -> Generator[duckdb.DuckDBPyConnection, None, None]:
    conn = duckdb.connect(database)
    try:
        if load_extensions_fn:
            load_extensions_fn(conn=conn)

        if attach_connections_fn:
            attach_connections_fn(conn=conn)

        yield conn
    finally:
        conn.close()
