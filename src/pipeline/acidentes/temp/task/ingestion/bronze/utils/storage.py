from functools import partial

from src.persistence.storage.utils import set_path
from ..constants.storage import (
    STORAGE_PATH,
    LOG_PATH,
)

set_storage_path = partial(
    set_path,
    base_path=STORAGE_PATH,
)
set_log_path = partial(
    set_path,
    base_path=LOG_PATH,
)
