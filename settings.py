"""settings.py"""

from os import getenv
from pathlib import Path
from typing import Literal
from pydantic import BaseModel, computed_field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

from constants import ROOT


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


env_profile = getenv("ENV", "dev")
ENV_FILE = f".env.{env_profile}"

postgres_settings = PostgresSettings(_env_file=ENV_FILE)
