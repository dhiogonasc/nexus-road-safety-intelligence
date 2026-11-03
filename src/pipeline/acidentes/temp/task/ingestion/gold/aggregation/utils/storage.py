from pathlib import Path
from typing import Optional

from src.persistence.storage.utils import set_path
from src.persistence.storage.settings import BucketSettings
from ..constants.storage import LAYER_PATH


def _set_table_storage_path(table_name: str):
    return Path(LAYER_PATH, table_name).as_posix()


def set_storage_path(
    table_name: str,
    settings: Optional[BucketSettings] = None,
):
    return set_path(
        base_path=_set_table_storage_path(table_name=table_name),
        settings=settings,
    )
