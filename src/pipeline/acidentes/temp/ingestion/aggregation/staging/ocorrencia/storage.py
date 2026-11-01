from functools import partial
from pathlib import Path

from src.persistence.storage.utils import set_path


SILVER_STORAGE_PATH = Path(
    "acidentes",
    "silver",
    "fact",
    "ocorrencia",
).as_posix()
set_silver_storage_path = partial(
    set_path,
    base_path=SILVER_STORAGE_PATH,
)