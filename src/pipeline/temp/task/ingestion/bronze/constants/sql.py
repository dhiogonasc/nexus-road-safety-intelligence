from src.shared.system.file import load_module
from ..sql import (
    stage,
)
from ..sql import copy_to_parquet
from ..sql import log_charge

STAGE_QUERIES_SQL = load_module(module=stage)
LOG_CHARGE_QUERIES_SQL = load_module(module=log_charge)
COPY_TO_PARQUET_QUERIES_SQL = load_module(module=copy_to_parquet)
