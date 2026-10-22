"""src/pipeline/index.py"""

from constants import AC_OCORRENCIA_DIR
from src.shared.model.pipeline import Asset
from src.pipeline.silver.acidentes.model import (
    dim_causa,
    dim_classificacao,
    dim_tipo,
    dim_condicao_metereologica,
    dim_coordenada,
    dim_tempo,
    dim_pista,
    dim_localizacao,
    fato_ocorrencia,
)
from src.pipeline.gold.acidentes.model import (
    agg_condicoes_via,
    agg_sazonalidade,
    agg_trechos_criticos,
)
from src.pipeline.silver.acidentes.transform import (
    upsert_acidentes_dim_causa,
    upsert_acidentes_dim_classificacao,
    upsert_acidentes_dim_tipo,
    upsert_acidentes_dim_condicao_metereologica,
    upsert_acidentes_dim_coordenada,
    upsert_acidentes_dim_tempo,
    upsert_acidentes_dim_pista,
    upsert_acidentes_dim_localizacao,
    upsert_acidentes_fato_ocorrencia,
)
from src.pipeline.gold.acidentes.load import (
    upsert_acidentes_agg_condicoes_via,
    upsert_acidentes_agg_sazonalidade,
    upsert_acidentes_agg_trechos_criticos,
)

asset_dim_causa = Asset(
    table=dim_causa,
    upsert_fn=upsert_acidentes_dim_causa,
)
asset_dim_tipo = Asset(
    table=dim_tipo,
    upsert_fn=upsert_acidentes_dim_tipo,
)
asset_dim_classificacao = Asset(
    table=dim_classificacao,
    upsert_fn=upsert_acidentes_dim_classificacao,
)
asset_dim_condicao = Asset(
    table=dim_condicao_metereologica,
    upsert_fn=upsert_acidentes_dim_condicao_metereologica,
)
asset_dim_coordenada = Asset(
    table=dim_coordenada,
    upsert_fn=upsert_acidentes_dim_coordenada,
)
asset_dim_tempo = Asset(
    table=dim_tempo,
    upsert_fn=upsert_acidentes_dim_tempo,
)
asset_dim_pista = Asset(
    table=dim_pista,
    upsert_fn=upsert_acidentes_dim_pista,
)
asset_dim_localizacao = Asset(
    table=dim_localizacao,
    upsert_fn=upsert_acidentes_dim_localizacao,
)
asset_fato_ocorrencia = Asset(
    table=fato_ocorrencia,
    upsert_fn=upsert_acidentes_fato_ocorrencia,
    depends_on=[
        asset_dim_causa,
        asset_dim_tipo,
        asset_dim_classificacao,
        asset_dim_condicao,
        asset_dim_coordenada,
        asset_dim_tempo,
        asset_dim_pista,
        asset_dim_localizacao,
    ],
)

asset_agg_condicoes_via = Asset(
    table=agg_condicoes_via,
    upsert_fn=upsert_acidentes_agg_condicoes_via,
)
asset_agg_sazonalidade = Asset(
    table=agg_sazonalidade,
    upsert_fn=upsert_acidentes_agg_sazonalidade,
)
asset_agg_trechos_criticos = Asset(
    table=agg_trechos_criticos,
    upsert_fn=upsert_acidentes_agg_trechos_criticos,
)

PIPELINE_CONFIG = {
    "acidentes": {
        "bronze": {
            "ocorrencias": str(AC_OCORRENCIA_DIR / "*.csv"),
        },
        "silver": [
            asset_dim_causa,
            asset_dim_tipo,
            asset_dim_classificacao,
            asset_dim_condicao,
            asset_dim_coordenada,
            asset_dim_tempo,
            asset_dim_pista,
            asset_dim_localizacao,
            asset_fato_ocorrencia,
        ],
        "gold": [
            asset_agg_condicoes_via,
            asset_agg_sazonalidade,
            asset_agg_trechos_criticos,
        ],
    }
}
