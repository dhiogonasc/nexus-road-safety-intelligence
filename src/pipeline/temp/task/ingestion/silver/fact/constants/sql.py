from src.shared.system.file import load_module
from ..sql import (
    upsert_by_partitions,
)
from ..sql import bootstrap
from ..sql import copy_to_parquet
from ..sql import create
from ..sql import log_charge

CREATE_QUERIES_SQL = load_module(module=create)
BOOTSTRAP_QUERIES_SQL = load_module(module=bootstrap)
LOG_CHARGE_QUERIES_SQL = load_module(module=log_charge)
COPY_TO_PARQUET_QUERIES_SQL = load_module(module=copy_to_parquet)
UPSERT_BY_PARTITIONS_QUERIES_SQL = load_module(module=upsert_by_partitions)
