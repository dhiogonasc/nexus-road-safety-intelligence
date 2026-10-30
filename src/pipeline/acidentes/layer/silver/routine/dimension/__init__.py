from .categoria import routine as categoria_routine
from .clima import routine as clima_routine
from .jurisdicao import routine as jurisdicao_routine
from .local import routine as local_routine
from .pista import routine as pista_routine
from .tempo import routine as tempo_routine

routines = [
    categoria_routine,
    clima_routine,
    jurisdicao_routine,
    local_routine,
    pista_routine,
    tempo_routine,
]
