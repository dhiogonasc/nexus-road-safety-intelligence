from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Dict, Literal

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

    @property
    def conn_string(self) -> str:
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
    def conn_alias(self) -> str:
        return self.DB_NAME

    @property
    def conn_type(self) -> str:
        return "POSTGRES"

    @property
    def attach_config(self) -> DatabaseAttachConfig:
        return DatabaseAttachConfig(
            conn_string=self.conn_string,
            conn_alias=self.conn_alias,
            conn_type=self.conn_type,
        )
