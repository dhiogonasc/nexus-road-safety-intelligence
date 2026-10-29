from typing import List

from .tempo import routine as tempo_routine
from .local import routine as local_routine
from .pista import routine as pista_routine
from .jurisdicao import routine as jurisdicao_routine
from .clima import routine as clima_routine
from .categoria import routine as categoria_routine

from src.shared.model.pipeline import Routine

routines: List[Routine] = [
    tempo_routine,
    local_routine,
    pista_routine,
    jurisdicao_routine,
    clima_routine,
    categoria_routine,
]
