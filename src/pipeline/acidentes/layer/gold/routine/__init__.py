from typing import List

from src.shared.model.pipeline import Routine

from .staging import routine as staging_routine
from .aggregation import routines as aggregation_routines

routines: List[Routine] = [staging_routine] + aggregation_routines