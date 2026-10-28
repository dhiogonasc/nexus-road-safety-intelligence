from typing import List

from .causa import routine as causa_routine
from .classificacao import routine as classificacao_routine
from .condicao_metereologica import routine as condicao_metereologica_routine
from .coordenada import routine as coordenada_routine
from .localizacao import routine as localizacao_routine
from .pista import routine as pista_routine
from .tempo import routine as tempo_routine
from .tipo import routine as tipo_routine

from src.shared.model.pipeline import Routine

routines: List[Routine] = [
    causa_routine,
    classificacao_routine,
    condicao_metereologica_routine,
    coordenada_routine,
    localizacao_routine,
    pista_routine,
    tempo_routine,
    tipo_routine,
]
