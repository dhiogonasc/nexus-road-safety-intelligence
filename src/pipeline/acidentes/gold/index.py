from src.shared.model.pipeline import (
    LayerSchemaConfig,
    PipelineAsset,
)
from pipeline.acidentes.gold.entity import (
    agg_condicoes_via,
    agg_sazonalidade,
    agg_trechos_criticos,
)
from src.pipeline.acidentes.gold.operation import (
    upsert_acidentes_agg_condicoes_via,
    upsert_acidentes_agg_sazonalidade,
    upsert_acidentes_agg_trechos_criticos,
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


config = LayerSchemaConfig(
    name="gold",
    assets=[
        asset_agg_condicoes_via,
        asset_agg_sazonalidade,
        asset_agg_trechos_criticos,
    ],
)
