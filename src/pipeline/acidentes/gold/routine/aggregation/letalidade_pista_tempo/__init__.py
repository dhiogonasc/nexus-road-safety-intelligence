from .operation import process_routine as routine_processor
from ...staging.ocorrencia import routine as staging_routine

routine = {
    "label": "agg_letalidade_pista_tempo",
    "processor": routine_processor,
    "depends_on": [staging_routine],
}
