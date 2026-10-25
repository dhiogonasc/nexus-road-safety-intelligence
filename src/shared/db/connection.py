"""src/shared/db/connection.py"""

from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Generator, Optional
import duckdb


@contextmanager
def create_connection(
    database: str,
    load_extensions_fn: Optional[Callable[[duckdb.DuckDBPyConnection], None]] = None,
    attach_connections_fn: Optional[Callable[[duckdb.DuckDBPyConnection], None]] = None,
) -> Generator[duckdb.DuckDBPyConnection, None, None]:
    """Gerencia a criacao de conexoes com entidades de persistencia (duckdb)"""

    Path(database).parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(
        database, 
        config={"max_memory": "4GB"}
    )
    try:
        if load_extensions_fn:
            load_extensions_fn(conn=conn)

        if attach_connections_fn:
            attach_connections_fn(conn=conn)

        yield conn
    finally:
        conn.close()
