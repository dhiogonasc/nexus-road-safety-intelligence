from src.shared.system.file import load_module

from . import (
    bootstrap,
    copy_to_parquet,
    create,
    log_charge,
    stage,
    upsert,
    upsert_by_partitions,
)

BOOTSTRAP_SQL = load_module(module=bootstrap)
COPY_TO_PARQUET_SQL = load_module(module=copy_to_parquet)
CREATE_SQL = load_module(module=create)
LOG_CHARGE_SQL = load_module(module=log_charge)
STAGE_SQL = load_module(module=stage)
UPSERT_SQL = load_module(module=upsert)
UPSERT_BY_PARTITIONS_SQL = load_module(module=upsert_by_partitions)
