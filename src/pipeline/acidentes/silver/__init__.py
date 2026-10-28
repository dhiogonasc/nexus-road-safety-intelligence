from src.shared.model.pipeline import Layer
from .routine import routines
from .operation import operations
from ..bronze import schema_routine as bronze_routine

layer = Layer(
    label="silver",
    operations=operations,
    routines=routines,
    depends_on=[bronze_routine],
)
