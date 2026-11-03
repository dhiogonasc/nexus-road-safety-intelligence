from src.shared.system.file import load_module
from ..sql import (
    create,
    bootstrap,
    copy_to_parquet,
    upsert_by_partitions,
)

CREATE_QUERIES_SQL = load_module(module=create)
BOOTSTRAP_QUERIES_SQL = load_module(module=bootstrap)
COPY_TO_PARQUET_QUERIES_SQL = load_module(module=copy_to_parquet)
UPSERT_BY_PARTITIONS_QUERIES_SQL = load_module(module=upsert_by_partitions)
