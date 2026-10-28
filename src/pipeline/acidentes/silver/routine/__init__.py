from typing import List

from src.shared.model.pipeline import Routine

from .staging import routine as staging_routine
from .dimension import routines as dimension_routines
from .fato import routines as fato_routines

routines: List[Routine] = [staging_routine] + dimension_routines + fato_routines