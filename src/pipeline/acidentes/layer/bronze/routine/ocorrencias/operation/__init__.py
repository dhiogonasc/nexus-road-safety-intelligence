from typing import List, Callable

from .registry import (
    create_table,
    copy_to_parquet,
    log_charge,
)

operations: List[Callable] = [
    create_table,
    copy_to_parquet,
    log_charge,
]
