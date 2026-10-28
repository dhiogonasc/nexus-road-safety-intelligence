from typing import Callable, List

from .registry import create, bootstrap, upsert, copy

operations: List[Callable] = [create, bootstrap, upsert, copy]
