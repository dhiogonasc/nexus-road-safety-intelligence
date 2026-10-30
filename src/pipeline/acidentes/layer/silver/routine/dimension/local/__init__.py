from .operation import process_routine as routine_processor
from ...staging.ocorrencia import routine as staging_routine

routine = {
    "label": "dim_local",
    "processor": routine_processor,
    "depends_on": [staging_routine],
}
