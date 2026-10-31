from functools import partial
from pathlib import Path

from src.persistence.storage.utils import set_path


STORAGE_PATH = Path(
    "acidentes",
    "silver",
    "dimension",
    "pista",
).as_posix()
set_storage_path = partial(
    set_path,
    base_path=STORAGE_PATH,
)
