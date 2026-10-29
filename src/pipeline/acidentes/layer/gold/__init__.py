from src.shared.model.pipeline import Layer
from .routine import routines
from .operation import operations

layer = Layer(
    label="gold",
    operations=operations,
    routines=routines,
    required_extensions=[
        "httpfs",
        "parquet",
    ],
)
