from functools import partial
from pathlib import Path

from src.persistence.storage.utils import set_path


STORAGE_PATH = Path(
    "acidentes",
    "gold",
    "aggregation",
    "letalidade_pista_clima",
).as_posix()
set_storage_path = partial(
    set_path,
    base_path=STORAGE_PATH,
)

DIM_STORAGE_BASE_PATH = Path(
    "acidentes",
    "silver",
    "dimension",
).as_posix()
set_dim_storage_path = partial(
    set_path,
    base_path=DIM_STORAGE_BASE_PATH,
)
