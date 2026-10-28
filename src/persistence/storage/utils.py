from pathlib import Path

from constants import ROOT
from .settings import BucketSettings


def set_path(base_path: str, settings: BucketSettings) -> str:
    BUCKET = f"s3://{settings.STORAGE_BUCKET}"
    s3 = Path(BUCKET, base_path).as_posix()
    local = Path(ROOT, base_path).as_posix()
    return s3 if settings else local