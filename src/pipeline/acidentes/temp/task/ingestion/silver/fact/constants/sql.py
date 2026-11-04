from src.shared.system.file import load_module
from ..sql import (
    create,
    bootstrap,
    log_charge,
    copy_to_parquet,
    upsert_by_partitions,
)

CREATE_QUERIES_SQL = load_module(module=create)
BOOTSTRAP_QUERIES_SQL = load_module(module=bootstrap)
LOG_CHARGE_QUERIES_SQL = load_module(module=log_charge)
COPY_TO_PARQUET_QUERIES_SQL = load_module(module=copy_to_parquet)
UPSERT_BY_PARTITIONS_QUERIES_SQL = load_module(module=upsert_by_partitions)
