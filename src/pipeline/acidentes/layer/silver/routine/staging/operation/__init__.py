from typing import List, Callable

from .registry import create_table

operations: List[Callable] = [create_table]
