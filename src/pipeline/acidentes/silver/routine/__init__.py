from typing import List

from src.shared.model.pipeline import Routine

from .staging import routines as staging_routines
from .dimension import routines as dimension_routines
from .fato import routines as fato_routines

routines: List[Routine] = staging_routines + dimension_routines + fato_routines