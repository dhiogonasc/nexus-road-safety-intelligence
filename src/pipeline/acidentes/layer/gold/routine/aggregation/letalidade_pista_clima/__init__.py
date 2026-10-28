from src.shared.model.pipeline import Routine
from .operation import operations
from ...staging import routine as staging_routine

routine = Routine(
    label="agg_letalidade_pista_clima",
    operations=operations,
    depends_on=[staging_routine],
)
