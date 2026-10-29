from src.shared.model.pipeline import Routine

from .operation import operations
from ...dimension import routines as dimension_routines

routine = Routine(
    label="ft_ocorrencia",
    operations=operations,
    depends_on=dimension_routines,
)
