from src.shared.system.file import load_module
from ..sql import (
    stage,
    log_charge,
    copt_to_parquet,
)

STAGE_QUERIES_SQL = load_module(module=stage)
LOG_CHARGE_QUERIES_SQL = load_module(module=log_charge)
COPY_TO_PARQUET_QUERIES_SQL = load_module(module=copt_to_parquet)
