from contextlib import contextmanager
from typing import Generator, List

import duckdb
from pydantic import BaseModel, Field

from .settings import (
    DatabaseAttachConfig,
    DuckDBSettings,
)


class DuckDBConnector(BaseModel):
    settings: DuckDBSettings = Field(default_factory=DuckDBSettings)
    extensions: List[str] = Field(default_factory=list)
    attach_configs: List[DatabaseAttachConfig] = Field(default_factory=list)

    def _load_extensions(self, conn: duckdb.DuckDBPyConnection) -> None:
        if self.extensions:
            for extension in self.extensions:
                try:
                    query = f"LOAD {extension};"
                    conn.execute(query=query)
                except duckdb.BinderException:
                    query = f"INSTALL {extension};\n LOAD {extension};"
                    conn.execute(query=query)

    def _attach_connections(self, conn: duckdb.DuckDBPyConnection) -> None:
        if self.attach_configs:
            for config in self.attach_configs:
                try:
                    query = f"ATTACH '{config.conn_string}' AS {config.conn_alias} (TYPE {config.conn_type});"
                    conn.execute(query=query)
                except duckdb.BinderException:
                    pass

    @contextmanager
    def create_connection(self) -> Generator[duckdb.DuckDBPyConnection, None, None]:
        conn = duckdb.connect(
            database=self.settings.database,
            config=self.settings.config,
        )
        try:
            self._load_extensions(conn=conn)
            self._attach_connections(conn=conn)
            yield conn
        finally:
            conn.close()
