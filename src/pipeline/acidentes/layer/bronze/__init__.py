from src.shared.model.pipeline import Layer
from .routine import routines

layer = Layer(
    label="bronze",
    routines=routines,
    required_extensions=[
        "httpfs",
        "parquet",
    ],
)
