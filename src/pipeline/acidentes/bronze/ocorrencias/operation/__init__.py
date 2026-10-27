from typing import Dict, Callable

from .registry import (
    create,
    copy,
    log,
)

operations: Dict[str, Callable] = {
    create.__name__: create,
    copy.__name__: copy,
    log.__name__: log,
}
