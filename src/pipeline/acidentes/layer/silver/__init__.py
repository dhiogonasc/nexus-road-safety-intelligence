from src.shared.model.pipeline import Layer
from .routine import routines
from .operation import operations
from ..bronze import layer as bronze_layer

layer = Layer(
    label="silver",
    routines=routines,
    operations=operations,
    depends_on=[bronze_layer],
    required_extensions=[
        "httpfs",
        "parquet",
    ],
)
