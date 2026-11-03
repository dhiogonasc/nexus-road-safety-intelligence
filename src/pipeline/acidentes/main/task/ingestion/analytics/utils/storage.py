from pathlib import Path
from typing import Optional

from src.persistence.storage.utils import set_path
from src.persistence.storage.settings import BucketSettings
from ..constants.storage import BASE_SOURCE_PATH


def _get_table_base_source_path(table_name: str):
    return Path(
        BASE_SOURCE_PATH,
        table_name,
    ).as_posix()


def get_table_source_path(
    table_name: str,
    settings: Optional[BucketSettings] = None,
):
    return set_path(
        base_path=_get_table_base_source_path(table_name=table_name),
        settings=settings,
    )
