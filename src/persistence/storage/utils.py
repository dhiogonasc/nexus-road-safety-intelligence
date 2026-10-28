from pathlib import Path
from typing import Optional

from constants import DB_DIR
from .settings import BucketSettings


def set_path(
    base_path: str,
    settings: Optional[BucketSettings] = None,
) -> str:
    if settings:
        bucket = f"s3://{settings.STORAGE_BUCKET}"
        return Path(bucket, base_path).as_posix()
    
    path = Path(DB_DIR, base_path)
    path.mkdir(parents=True, exist_ok=True)
    return path.as_posix()
