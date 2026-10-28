from constants import AC_OCORRENCIAS_DIR
from src.shared.model.pipeline import Routine
from .operation import operations

routine = Routine(
    label="raw_ocorrencias",
    operations=operations,
)
