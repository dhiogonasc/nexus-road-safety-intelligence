from src.shared.model.pipeline import Layer

from .operation import operations
from .routine import routines

layer = Layer(
    label="bronze",
    routines=routines,
    operations=operations,
    required_extensions=[
        "httpfs",
        "parquet",
    ],
)
