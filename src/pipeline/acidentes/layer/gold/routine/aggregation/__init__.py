from typing import List

from .dispersao_geo_temporal import routine as dispersao_geo_temporal_routine
from src.shared.model.pipeline import Routine

routines: List[Routine] = [dispersao_geo_temporal_routine]
