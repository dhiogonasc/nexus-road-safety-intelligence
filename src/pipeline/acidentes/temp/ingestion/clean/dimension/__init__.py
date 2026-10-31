from .categoria import task as dim_categoria_task
from .clima import task as dim_clima_task
from .jurisdicao import task as dim_jurisdicao_task
from .local import task as dim_local_task
from .pista import task as dim_pista_task
from .tempo import task as dim_tempo_task

dim_tasks = [
    dim_categoria_task,
    dim_clima_task,
    dim_jurisdicao_task,
    dim_local_task,
    dim_pista_task,
    dim_tempo_task,
]