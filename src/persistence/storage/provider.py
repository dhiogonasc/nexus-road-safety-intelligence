from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from constants import DB_DIR
from src.persistence.storage.settings import StorageSettings


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
