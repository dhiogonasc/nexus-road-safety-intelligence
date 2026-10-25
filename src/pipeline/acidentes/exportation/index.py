from settings import postgres_settings
from src.shared.model.pipeline import (
    LayerSchemaConfig,
    PipelineAsset,
)
from pipeline.acidentes.exportation.entity import (
    agg_condicoes_via as exportation_agg_condicoes_via,
    agg_sazonalidade as exportation_agg_sazonalidade,
    agg_trechos_criticos as exportation_agg_trechos_criticos,
)
from pipeline.acidentes.exportation.operation import (
    upsert_exportation_acidentes_agg_condicoes_via,
    upsert_exportation_acidentes_agg_sazonalidade,
    upsert_exportation_acidentes_agg_trechos_criticos,
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

config = LayerSchemaConfig(
    catalog=postgres_settings.DB_NAME,
    name="analytics",
    assets=[
        asset_exportation_agg_condicoes_via,
        asset_exportation_agg_sazonalidade,
        asset_exportation_agg_trechos_criticos,
    ],
)
