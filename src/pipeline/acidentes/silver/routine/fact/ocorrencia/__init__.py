from .operation import process_routine as routine_processor
from ...dimension import routines as dimension_routines

routine = {
    "label": "dim_tempo",
    "processor": routine_processor,
    "depends_on": dimension_routines,
}
