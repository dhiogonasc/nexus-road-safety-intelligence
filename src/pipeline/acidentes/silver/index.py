from src.shared.model.pipeline import (
    LayerSchemaConfig,
    PipelineAsset,
)
from pipeline.acidentes.silver.entity import schema
from pipeline.acidentes.silver.entity import (
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
from src.pipeline.acidentes.silver.operation import (
    upsert_acidentes_dim_causa,
    upsert_acidentes_dim_classificacao,
    upsert_acidentes_dim_tipo,
    upsert_acidentes_dim_condicao_metereologica,
    upsert_acidentes_dim_coordenada,
    upsert_acidentes_dim_tempo,
    upsert_acidentes_dim_pista,
    upsert_acidentes_dim_localizacao,
    upsert_acidentes_fato_ocorrencia_per_uf,
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
    upsert_fn=upsert_acidentes_fato_ocorrencia_per_uf,
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
config = LayerSchemaConfig(
    name="silver",
    assets=[
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
)
