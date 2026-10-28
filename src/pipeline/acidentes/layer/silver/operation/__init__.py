from typing import Callable, List

from .registry import create

operations: List[Callable] = [create]
