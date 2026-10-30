from functools import partial
from pathlib import Path

from src.persistence.storage.utils import set_path

STORAGE_PATH = Path(
    "acidentes",
    "bronze",
    "ocorrencias",
)
set_storage_path = partial(
    set_path,
    base_path=STORAGE_PATH,
)

LOG_PATH = Path(
    "acidentes",
    "bronze",
    "log",
    "ocorrencias",
)
set_log_path = partial(
    set_path,
    base_path=LOG_PATH,
)