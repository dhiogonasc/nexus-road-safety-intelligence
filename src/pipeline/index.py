from constants import AC_OCORRENCIA_DIR
from src.pipeline.gold.acidentes.load import (
    create_acidentes_agg_localidade,
    create_acidentes_agg_sazonalidade_anual,
    create_acidentes_agg_sazonalidade_diaria,
    create_acidentes_agg_sazonalidade_mensal,
)
from src.pipeline.silver.acidentes.transform import (
    create_acidentes_dim_classificacao,
    create_acidentes_dim_localizacao,
    create_acidentes_dim_pista,
    create_acidentes_dim_tempo,
    create_acidentes_fato_ocorrencia,
)

PIPELINE_CONFIG = {
    # schema
    "acidentes": {
        # stage
        "bronze": {
            "ocorrencias": str(AC_OCORRENCIA_DIR / "*.csv"),
        },
        "silver": {
            "dim_tempo": {
                "fn": create_acidentes_dim_tempo,
                "depends_on": [],
            },
            "dim_localizacao": {
                "fn": create_acidentes_dim_localizacao,
                "depends_on": [],
            },
            "dim_pista": {
                "fn": create_acidentes_dim_pista,
                "depends_on": [],
            },
            "dim_classificacao": {
                "fn": create_acidentes_dim_classificacao,
                "depends_on": [],
            },
            "fato_ocorrencia": {
                "fn": create_acidentes_fato_ocorrencia,
                "depends_on": [
                    "dim_tempo",
                    "dim_localizacao",
                    "dim_pista",
                    "dim_classificacao",
                ],
            },
        },
        "gold": {
            "agg_sazonalidade_anual": {
                "fn": create_acidentes_agg_sazonalidade_anual,
                "target": "acidentes_sazonalidade_anual",
                "primary_keys": ["id"],
            },
            "agg_sazonalidade_mensal": {
                "fn": create_acidentes_agg_sazonalidade_mensal,
                "target": "acidentes_sazonalidade_mensal",
                "primary_keys": ["id"],
            },
            "agg_sazonalidade_diaria": {
                "fn": create_acidentes_agg_sazonalidade_diaria,
                "target": "acidentes_sazonalidade_diaria",
                "primary_keys": ["id"],
            },
            "agg_localidade": {
                "fn": create_acidentes_agg_localidade,
                "target": "acidentes_localidade",
                "primary_keys": ["id"],
            },
        },
    }
}
