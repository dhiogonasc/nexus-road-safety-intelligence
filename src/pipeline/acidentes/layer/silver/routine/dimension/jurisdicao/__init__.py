from .operation import process_routine as routine_processor
from ...staging import routine as staging_routine

routine = {
    "label": "dim_jurisdicao",
    "processor": routine_processor,
    "depends_on": [staging_routine],
}
