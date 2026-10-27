from src.shared.model.pipeline import SchemaRoutine
from .routine import routines
from .operation import operations
from ..bronze import schema_routine as bronze_routine

schema_routine = SchemaRoutine(
    operations=operations,
    routines=routines,
    depends_on=[bronze_routine],
)
