from src.shared.model.pipeline import Routine

from .operation import operations
from ...staging import routine as staging_routine

routine = Routine(
    label="dim_categoria",
    operations=operations,
    depends_on=[staging_routine],
)