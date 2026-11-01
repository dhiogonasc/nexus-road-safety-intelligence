from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from constants import ROOT, DB_DIR

@dataclass
class DuckDBSettings:
    """Configuração DuckDB"""

    DIRECTORY: str = Path(DB_DIR).as_posix()

    def database(self, name: str, db_dir: Optional[str] = None) -> str:
        """Chave de conexão"""
        if db_dir:
            Path(self.DIRECTORY, db_dir).mkdir(parents=True, exist_ok=True)
            return Path(self.DIRECTORY, db_dir, f"{name}.db").as_posix()
        return Path(self.DIRECTORY, f"{name}.db").as_posix()


settings_temp = DuckDBSettings()

from typing import Literal
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

ENV_FILE = ROOT / ".env"
env_file = ENV_FILE if ENV_FILE.exists() else None

class PostgresSettings(BaseSettings):
    """Configura Postgres"""

    ENV: Literal["dev", "prod"] = "dev"
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    ENV: Literal["dev", "prod"] = "dev"

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def conn_string(self) -> str:
        """Define o sslmode dinamicamente com base no nome do _env_file utilizado"""
        sslmode = "require" if self.ENV == "prod" else "prefer"

        return (
            f"dbname={self.DB_NAME} "
            f"user={self.DB_USER} "
            f"password={self.DB_PASSWORD} "
            f"host={self.DB_HOST} "
            f"port={self.DB_PORT} "
            f"sslmode={sslmode}"
        )


settings_main = PostgresSettings()
