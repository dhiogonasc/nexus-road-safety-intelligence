import os
from typing import Literal
from constants import DATABASE_DIR
from pydantic_settings import BaseSettings, SettingsConfigDict

env_profile = os.getenv("ENV")
env_file = f".env.{env_profile}"

duckdb_path = DATABASE_DIR / "rsi_pei6.db"
duckcb_extensions = [
    "postgres",
]


class Settings(BaseSettings):
    ENV: Literal["dev", "prod"] = env_profile

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    DUCKDB_PATH: str = str(duckdb_path)
    DUCKDB_EXTENSIONS: list[str] = duckcb_extensions

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def postgres_conn_string(self) -> str:
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
