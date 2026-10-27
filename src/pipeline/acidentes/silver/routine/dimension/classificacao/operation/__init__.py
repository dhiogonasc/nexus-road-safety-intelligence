from typing import Dict, Callable

from .registry import (
    create,
    bootstrap,
    upsert,
    copy,
)

operations: Dict[str, Callable] = {
    create.__name__: create,
    bootstrap.__name__: bootstrap,
    upsert.__name__: upsert,
    copy.__name__: copy,
}