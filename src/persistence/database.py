from contextlib import contextmanager
from pandas import DataFrame
from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, Generator, List, Literal

import duckdb

from constants import DB_DIR


class DuckDBSettings(BaseModel):
    name: str = "default"
    directory: str = Path(DB_DIR).as_posix()
    max_memory: str = "4GB"
    enable_object_cache: bool = False

    @property
    def database(self) -> str:
        filename = f"{self.name}.db"
        return Path(self.directory, filename).as_posix()

    @property
    def config(self) -> Dict[str, str]:
        return {
            "max_memory": self.max_memory,
            "enable_object_cache": self.enable_object_cache,
        }


class DatabaseAttachConfig(BaseModel):
    conn_string: str
    conn_alias: str
    conn_type: str


class DatabaseSettings(BaseSettings):
    ENV: Literal["dev", "prod"] = "dev"

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def conn_alias(self) -> str:
        return self.DB_NAME

    @property
    def _conn_string(self) -> str:
        sslmode = "prefer" if self.ENV == "dev" else "require"

        return (
            f"dbname={self.DB_NAME} "
            f"user={self.DB_USER} "
            f"password={self.DB_PASSWORD} "
            f"host={self.DB_HOST} "
            f"port={self.DB_PORT} "
            f"sslmode={sslmode}"
        )

    @property
    def _conn_type(self) -> str:
        return "POSTGRES"

    @property
    def attach_config(self) -> DatabaseAttachConfig:
        return DatabaseAttachConfig(
            conn_alias=self.conn_alias,
            conn_string=self._conn_string,
            conn_type=self._conn_type,
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


class DuckDBProvider(BaseModel):
    connector: DuckDBConnector = Field(default_factory=DuckDBConnector)

    def execute_query(self, sql: str, **kwargs) -> duckdb.DuckDBPyRelation:
        with self.connector.create_connection() as conn:
            return conn.execute(query=sql.format(**kwargs))

    def fecth_df(self, sql: str, **kwargs) -> DataFrame:
        with self.connector.create_connection() as conn:
            return conn.execute(query=sql.format(**kwargs)).fetchdf()
