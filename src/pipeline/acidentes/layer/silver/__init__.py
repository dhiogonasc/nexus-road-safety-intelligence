from src.shared.model.pipeline import Layer
from .routine import routines
from .operation import operations

layer = Layer(
    label="silver",
    routines=routines,
    operations=operations,
    required_extensions=[
        "httpfs",
        "parquet",
    ],
)
