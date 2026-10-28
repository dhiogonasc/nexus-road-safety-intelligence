from src.shared.model.pipeline import Layer
from .routine import routines
from .operation import operations
from ..silver import layer as silver_layer

layer = Layer(
    label="gold",
    operations=operations,
    routines=routines,
    depends_on=[silver_layer],
    required_extensions=[
        "httpfs",
        "parquet",
    ],
)
