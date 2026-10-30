from pydantic_settings import BaseSettings, SettingsConfigDict

from constants import ROOT

ENV_FILE = ROOT / ".env"
env_file = ENV_FILE if ENV_FILE.exists() else None

class BucketSettings(BaseSettings):
    """Configuração S3 Bucket"""

    STORAGE_BUCKET: str = "rsi-bucket"
    STORAGE_ENDPOINT: str = "http://localhost:3900"
    STORAGE_ACCESS_KEY_ID: str
    STORAGE_SECRET_ACCESS_KEY: str
    STORAGE_REGION: str = "nexus"

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = BucketSettings()