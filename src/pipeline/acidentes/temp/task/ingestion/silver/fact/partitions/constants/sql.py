from src.shared.system.file import load_module
from ..sql import (
    create_temp,
    upsert_temp,
    upsert_ft,
)

CREATE_TEMP_QUERIES_SQL = load_module(module=create_temp)
UPSERT_TEMP_QUERIES_SQL = load_module(module=upsert_temp)
UPSERT_FT_QUERIES_SQL = load_module(module=upsert_ft)

