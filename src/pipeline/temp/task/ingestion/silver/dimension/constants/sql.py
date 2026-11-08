from src.shared.system.file import load_module
from ..sql import (
    upsert,
)
from ..sql import bootstrap
from ..sql import copy_to_parquet
from ..sql import create

UPSERT_QUERIES_SQL = load_module(module=upsert)
CREATE_QUERIES_SQL = load_module(module=create)
BOOTSTRAP_QUERIES_SQL = load_module(module=bootstrap)
COPY_TO_PARQUET_QUERIES_SQL = load_module(module=copy_to_parquet)
