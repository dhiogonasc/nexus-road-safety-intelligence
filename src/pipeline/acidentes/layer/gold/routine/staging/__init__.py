from src.shared.model.pipeline import Routine
from .operation import operations

routine = Routine(
    label="stg",
    operations=operations
)
