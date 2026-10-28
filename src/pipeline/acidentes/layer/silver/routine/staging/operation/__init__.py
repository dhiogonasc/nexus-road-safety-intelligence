from typing import List, Callable

from .registry import create

operations: List[Callable] = [create]
