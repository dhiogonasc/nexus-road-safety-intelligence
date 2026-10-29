from typing import List, Callable

from .registry import (
    create_table,
    upsert_table,
    bootstrap_table,
    copy_to_parquet,
)

operations: List[Callable] = [
    create_table,
    upsert_table,
    bootstrap_table,
    copy_to_parquet,
]
