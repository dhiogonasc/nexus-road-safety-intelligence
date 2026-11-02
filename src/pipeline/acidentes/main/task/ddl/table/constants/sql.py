from src.shared.system.file import load_module
from ..sql import (
    fact,
    dimension,
    aggregation,
)

QUERIES_SQL = {
    **load_module(module=fact),
    **load_module(module=dimension),
    **load_module(module=aggregation),
}
