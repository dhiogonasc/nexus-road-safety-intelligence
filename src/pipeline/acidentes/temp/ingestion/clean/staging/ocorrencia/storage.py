from functools import partial
from pathlib import Path

from src.persistence.storage.utils import set_path


STORAGE_PATH = Path(
    "acidentes",
    "silver",
    "staging",
    "ocorrencia",
).as_posix()
set_storage_path = partial(
    set_path,
    base_path=STORAGE_PATH,
)

LOG_PATH = Path(
    "acidentes",
    "silver",
    "staging",
    "log",
    "ocorrencia",
).as_posix()
set_log_path = partial(
    set_path,
    base_path=LOG_PATH,
)

RAW_STORAGE_PATH = Path(
    "acidentes",
    "bronze",
    "ocorrencias",
).as_posix()
set_raw_storage_path = partial(
    set_path,
    base_path=RAW_STORAGE_PATH,
)

RAW_LOG_PATH = Path(
    "acidentes",
    "bronze",
    "log",
    "ocorrencias",
).as_posix()
set_raw_log_path = partial(
    set_path,
    base_path=RAW_LOG_PATH,
)