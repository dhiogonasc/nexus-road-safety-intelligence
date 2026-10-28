from typing import List

from .dispersao_geo_temporal import routine as dispersao_geo_temporal_routine
from .letalidade_clima_tempo import routine as letalidade_clima_tempo_routine
from .letalidade_pista_clima import routine as letalidade_pista_clima_routine
from .letalidade_pista_tempo import routine as letalidade_pista_tempo_routine
from .trechos_criticos import routine as trechos_criticos_routine
from src.shared.model.pipeline import Routine

routines: List[Routine] = [
    dispersao_geo_temporal_routine,
    letalidade_pista_tempo_routine,
    letalidade_clima_tempo_routine,
    letalidade_pista_clima_routine,
    trechos_criticos_routine,
]
