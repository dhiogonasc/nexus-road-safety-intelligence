from typing import Dict, Callable

from .registry import (
    create,
    bootstrap,
    upsert,
    copy,
    fetch_last_uf_charged,
)

operations: Dict[str, Callable] = {
    create.__name__: create,
    bootstrap.__name__: bootstrap,
    upsert.__name__: upsert,
    copy.__name__: copy,
    fetch_last_uf_charged.__name__: fetch_last_uf_charged,
}
