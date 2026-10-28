from pydantic_settings import BaseSettings, SettingsConfigDict


class BucketSettings(BaseSettings):
    """Configuração S3 Bucket"""

    STORAGE_BUCKET: str
    STORAGE_ENDPOINT: str
    STORAGE_ACCESS_KEY_ID: str
    STORAGE_SECRET_ACCESS_KEY: str
    STORAGE_REGION: str

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_env_file = str(kwargs.get("_env_file", ""))