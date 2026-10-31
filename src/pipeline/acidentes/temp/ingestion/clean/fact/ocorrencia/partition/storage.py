from functools import partial
from pathlib import Path

from src.persistence.storage.utils import set_path


STG_STORAGE_PATH = Path(
    "acidentes",
    "silver",
    "staging",
    "ocorrencia",
).as_posix()
set_staging_storage_path = partial(
    set_path,
    base_path=STG_STORAGE_PATH,
)

STG_LOG_PATH = Path(
    "acidentes",
    "silver",
    "staging",
    "log",
    "ocorrencia",
).as_posix()
set_staging_log_path = partial(
    set_path,
    base_path=STG_LOG_PATH,
)