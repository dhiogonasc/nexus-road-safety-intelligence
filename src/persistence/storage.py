from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from constants import DB_DIR



class StorageSettings(BaseSettings):
    STORAGE_BUCKET: str = "bucket"
    STORAGE_ENDPOINT: str = "http://localhost:3900"
    STORAGE_REGION: str = "region"
    STORAGE_ACCESS_KEY_ID: str = ""
    STORAGE_SECRET_ACCESS_KEY: str = ""

    @property
    def conn_config(self) -> str:
        return (
            f"ENDPOINT '{self.STORAGE_ENDPOINT}', \n"
            f"KEY_ID '{self.STORAGE_ACCESS_KEY_ID}', \n"
            f"SECRET '{self.STORAGE_SECRET_ACCESS_KEY}', \n"
            f"REGION '{self.STORAGE_REGION}', \n"
        )

    @property
    def base_uri(self) -> str:
        return f"s3://{self.STORAGE_BUCKET}"


class StorageProvider(BaseModel):
    table_name: str
    base_path: str
    settings: Optional[StorageSettings] = None

    def _get_domain_storage_base_path(self) -> str:
        if self.settings:
            bucket = self.settings.base_uri.rstrip("/")
            return f"{bucket}/{self.base_path}"

        path = Path(DB_DIR, self.base_path)
        path.mkdir(parents=True, exist_ok=True)
        return path.as_posix()

    def get_storage_path(self) -> str:
        base = self._get_domain_storage_base_path()
        if base.startswith("s3://"):
            return f"{base.rstrip('/')}/{self.table_name}"

        path = Path(base, self.table_name)
        path.mkdir(parents=True, exist_ok=True)
        return Path(path).as_posix()

    def get_log_path(self) -> str:
        base = self._get_domain_storage_base_path()
        if base.startswith("s3://"):
            return f"{base.rstrip('/')}/log/{self.table_name}"

        path = Path(base, "log", self.table_name)
        path.mkdir(parents=True, exist_ok=True)
        return Path(path).as_posix()
