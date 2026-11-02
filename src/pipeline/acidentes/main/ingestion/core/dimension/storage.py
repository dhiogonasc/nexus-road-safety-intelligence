from functools import partial
from pathlib import Path

from src.persistence.storage.utils import set_path

BASE_STORAGE_PATH = Path(
    "acidentes",
    "silver",
    "dimension",
).as_posix()


def set_storage_path_fn(table_name: str):
    base_path = Path(
        BASE_STORAGE_PATH,
        table_name,
    ).as_posix()
    return partial(
        set_path,
        base_path=base_path,
    )
