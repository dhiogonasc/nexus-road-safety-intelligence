from os import getenv
from pathlib import Path
from typing import Literal
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

from constants import DATABASE_DIR

env_profile = getenv("ENV", "dev")
ENV_FILE = f".env.{env_profile}"


class Settings(BaseSettings):
    """Configura as entidades de persistência"""

    ENV: Literal["dev", "prod"] = env_profile

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DUCKDB_PATH: str = str(DATABASE_DIR)
    DUCKDB_EXTENSIONS: list[str] = ["postgres"]

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def domain_db_path(self, domain: str) -> str:
        """Define a chave de conexão duckdb"""
        domain_db = f"{domain}.db"
        duckdb_path = Path(self.DUCKDB_PATH)
        return str(duckdb_path / domain_db)

    @property
    def postgres_conn_string(self) -> str:
        """Define a chave de conexão postgres em produção ou desenvolvimento"""
        sslmode = "require" if self.ENV == "prod" else "prefer"
        return (
            f"dbname={self.DB_NAME} "
            f"user={self.DB_USER} "
            f"password={self.DB_PASSWORD} "
            f"host={self.DB_HOST} "
            f"port={self.DB_PORT} "
            f"sslmode={sslmode}"
        )


settings = Settings()
