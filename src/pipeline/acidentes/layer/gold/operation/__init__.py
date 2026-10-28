from typing import Callable, Dict

from .registry import create

operations: Dict[str, Callable] = {
    create.__name__: create,
}
