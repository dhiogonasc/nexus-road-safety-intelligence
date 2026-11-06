from pathlib import Path
from typing import Optional

from constants import DB_DIR
from .settings import BucketSettings


def _get_storage_base_path(
    base_path: str,
    settings: Optional[BucketSettings] = None,
) -> str:
    if settings:
        bucket = f"s3://{settings.STORAGE_BUCKET}"
        clean_base = base_path.lstrip("/")
        return f"{bucket}/{clean_base}"

    path = Path(DB_DIR, base_path)
    path.mkdir(parents=True, exist_ok=True)
    return path.as_posix()


def get_storage_path(
    table_name: str,
    base_path: str,
    settings: Optional[BucketSettings] = None,
):
    return _get_storage_base_path(
        base_path=Path(
            base_path,
            table_name,
        ).as_posix(),
        settings=settings,
    )


def get_log_path(
    table_name: str,
    base_path: str,
    settings: Optional[BucketSettings] = None,
):
    return _get_storage_base_path(
        base_path=Path(
            base_path,
            "log",
            table_name,
        ).as_posix(),
        settings=settings,
    )
