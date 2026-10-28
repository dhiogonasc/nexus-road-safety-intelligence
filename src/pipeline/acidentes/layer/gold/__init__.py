from src.shared.model.pipeline import SchemaRoutine
from .routine import routines
from .operation import operations
from ..silver import schema_routine as silver_routine

schema_routine = SchemaRoutine(
    
    operations=operations,
    routines=routines,
    depends_on=[silver_routine],
)
