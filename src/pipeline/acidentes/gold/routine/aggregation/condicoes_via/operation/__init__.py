from typing import Callable, Dict

from .registry import bootstrap, create, upsert, copy

operations: Dict[str, Callable] = {
    bootstrap.__name__: bootstrap,
    copy.__name__: copy,
    create.__name__: create,
    upsert.__name__: upsert,
}
