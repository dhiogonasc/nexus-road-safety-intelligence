from typing import List, Callable

from .registry import create, copy, log

operations: List[Callable] = [create, copy, log]
