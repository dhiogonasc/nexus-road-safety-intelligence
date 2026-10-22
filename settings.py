"""settings.py"""

from os import getenv
from pathlib import Path
from typing import Literal
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class DuckDBSettings(BaseSettings):
    """Configura DuckDB"""

    PATH: str = str(Path().resolve(__file__) / "db")
    EXTENSIONS: list[str] = [
        "postgres",
        "httpfs",
        "parquet",
    ]

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def get_database_path(self, domain: str) -> str:
        """Define a chave de conexão duckdb"""
        return str(Path(self.PATH) / f"{domain}.db")


class PostgresSettings(BaseSettings):
    """Configura Postgres"""

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    ENV: Literal["dev", "prod"] = "dev"

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_env_file = str(kwargs.get("_env_file", ""))

    @property
    def postgres_conn_string(self) -> str:
        """Define o sslmode dinamicamente com base no nome do _env_file utilizado"""
        sslmode = "require" if "prod" in self._current_env_file else "prefer"

        return (
            f"dbname={self.DB_NAME} "
            f"user={self.DB_USER} "
            f"password={self.DB_PASSWORD} "
            f"host={self.DB_HOST} "
            f"port={self.DB_PORT} "
            f"sslmode={sslmode}"
        )


class BucketSettings(BaseSettings):
    """Configura a bucket"""

    STORAGE_BUCKET: str
    STORAGE_ENDPOINT: str
    STORAGE_ACCESS_KEY_ID: str
    STORAGE_SECRET_ACCESS_KEY: str
    STORAGE_REGION: str

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )


env_profile = getenv("ENV", "dev")
ENV_FILE = f".env.{env_profile}"

duckdb_settings = DuckDBSettings(_env_file=ENV_FILE)
postgres_settings = PostgresSettings(_env_file=ENV_FILE)
bucket_settings = BucketSettings(_env_file=ENV_FILE)
