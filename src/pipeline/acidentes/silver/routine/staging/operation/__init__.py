from typing import Dict, Callable

from .registry import fetch

operations: Dict[str, Callable] = {fetch.__name__: fetch}
