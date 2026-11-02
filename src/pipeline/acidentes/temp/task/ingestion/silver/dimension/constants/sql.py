from src.shared.system.file import load_module
from ..sql import (
    create,
    bootstrap,
    upsert,
    copy_to_parquet,
)

CREATE_QUERIES_SQL = load_module(module=create)
BOOTSTRAP_QUERIES_SQL = load_module(module=bootstrap)
UPSERT_QUERIES_SQL = load_module(module=upsert)
COPY_TO_PARQUET_QUERIES_SQL = load_module(module=copy_to_parquet)
