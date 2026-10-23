"""src/pipeline/acidentes/index.py"""

from constants import AC_OCORRENCIA_DIR
from src.shared.model.pipeline import (
    DomainPipelineConfig,
    PipelineAsset,
)
from src.pipeline.acidentes.silver.table import (
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
from src.pipeline.acidentes.gold.table import (
    agg_condicoes_via,
    agg_sazonalidade,
    agg_trechos_criticos,
)
from src.pipeline.acidentes.gold.exportation.table import (
    agg_condicoes_via as exportation_agg_condicoes_via,
    agg_sazonalidade as exportation_agg_sazonalidade,
    agg_trechos_criticos as exportation_agg_trechos_criticos,
)
from src.pipeline.acidentes.silver.operation import (
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
from src.pipeline.acidentes.gold.operation import (
    upsert_acidentes_agg_condicoes_via,
    upsert_acidentes_agg_sazonalidade,
    upsert_acidentes_agg_trechos_criticos,
)
from src.pipeline.acidentes.gold.exportation.operation import (
    upsert_exportation_acidentes_agg_condicoes_via,
    upsert_exportation_acidentes_agg_sazonalidade,
    upsert_exportation_acidentes_agg_trechos_criticos,
)

asset_dim_causa = PipelineAsset(
    table=dim_causa,
    upsert_fn=upsert_acidentes_dim_causa,
)
asset_dim_tipo = PipelineAsset(
    table=dim_tipo,
    upsert_fn=upsert_acidentes_dim_tipo,
)
asset_dim_classificacao = PipelineAsset(
    table=dim_classificacao,
    upsert_fn=upsert_acidentes_dim_classificacao,
)
asset_dim_condicao = PipelineAsset(
    table=dim_condicao_metereologica,
    upsert_fn=upsert_acidentes_dim_condicao_metereologica,
)
asset_dim_coordenada = PipelineAsset(
    table=dim_coordenada,
    upsert_fn=upsert_acidentes_dim_coordenada,
)
asset_dim_tempo = PipelineAsset(
    table=dim_tempo,
    upsert_fn=upsert_acidentes_dim_tempo,
)
asset_dim_pista = PipelineAsset(
    table=dim_pista,
    upsert_fn=upsert_acidentes_dim_pista,
)
asset_dim_localizacao = PipelineAsset(
    table=dim_localizacao,
    upsert_fn=upsert_acidentes_dim_localizacao,
)
asset_fato_ocorrencia = PipelineAsset(
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

asset_agg_condicoes_via = PipelineAsset(
    table=agg_condicoes_via,
    upsert_fn=upsert_acidentes_agg_condicoes_via,
)
asset_agg_sazonalidade = PipelineAsset(
    table=agg_sazonalidade,
    upsert_fn=upsert_acidentes_agg_sazonalidade,
)
asset_agg_trechos_criticos = PipelineAsset(
    table=agg_trechos_criticos,
    upsert_fn=upsert_acidentes_agg_trechos_criticos,
)

asset_exportation_agg_condicoes_via = PipelineAsset(
    table=exportation_agg_condicoes_via,
    upsert_fn=upsert_exportation_acidentes_agg_condicoes_via,
)
asset_exportation_agg_sazonalidade = PipelineAsset(
    table=exportation_agg_sazonalidade,
    upsert_fn=upsert_exportation_acidentes_agg_sazonalidade,
)
asset_exportation_agg_trechos_criticos = PipelineAsset(
    table=exportation_agg_trechos_criticos,
    upsert_fn=upsert_exportation_acidentes_agg_trechos_criticos,
)

PIPELINE_CONFIG = DomainPipelineConfig(
    bronze={
        "ocorrencias": str(AC_OCORRENCIA_DIR / "*.csv"),
    },
    silver=[
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
    gold=[
        asset_agg_condicoes_via,
        asset_agg_sazonalidade,
        asset_agg_trechos_criticos,
    ],
    exportation=[
        asset_exportation_agg_condicoes_via,
        asset_exportation_agg_sazonalidade,
        asset_exportation_agg_trechos_criticos,
    ],
)
