from typing import Callable, List

from .registry import create_schema

operations: List[Callable] = [create_schema]
