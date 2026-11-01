from .dispersao_geo_temporal import task as agg_dispersao_geo_temporal_task
from .letalidade_clima_tempo import task as agg_letalidade_clima_tempo_task
from .letalidade_pista_clima import task as agg_letalidade_pista_clima
from .letalidade_pista_tempo import task as agg_letalidade_pista_tempo
from .trechos_criticos import task as agg_trechos_criticos_task

agg_tasks = [
    agg_dispersao_geo_temporal_task,
    agg_letalidade_clima_tempo_task,
    agg_letalidade_pista_clima,
    agg_letalidade_pista_tempo,
    agg_trechos_criticos_task,
]