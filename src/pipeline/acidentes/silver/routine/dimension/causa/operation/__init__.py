from typing import List, Callable

from .registry import create, bootstrap, upsert, copy

operations: List[Callable] = [create, bootstrap, upsert, copy]
