"""src/pipeline/index.py"""

from constants import AC_OCORRENCIA_DIR
from src.pipeline.gold.acidentes.load import (
    create_acidentes_agg_localidade,
    create_acidentes_agg_condicoes_via,
    create_acidentes_agg_sazonalidade,
    create_acidentes_agg_trechos_criticos,
)
from src.pipeline.silver.acidentes.transform import (
    create_acidentes_dim_causa,
    create_acidentes_dim_classificacao,
    create_acidentes_dim_coordenada,
    create_acidentes_dim_localizacao,
    create_acidentes_dim_pista,
    create_acidentes_dim_tempo,
    create_acidentes_dim_tipo,
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
            "dim_coordenada": {
                "fn": create_acidentes_dim_coordenada,
                "depends_on": [],
            },
            "dim_pista": {
                "fn": create_acidentes_dim_pista,
                "depends_on": [],
            },
            "dim_causa": {
                "fn": create_acidentes_dim_causa,
                "depends_on": [],
            },
            "dim_tipo": {
                "fn": create_acidentes_dim_tipo,
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
                    "dim_coordenada",
                    "dim_pista",
                    "dim_causa",
                    "dim_tipo",
                    "dim_classificacao",
                ],
            },
        },
        "gold": {
            "agg_localidade": {
                "fn": create_acidentes_agg_localidade,
                "target": "acidentes_agg_localidade",
                "primary_keys": ["id"],
            },
            "agg_condicoes_via": {
                "fn": create_acidentes_agg_condicoes_via,
                "target": "acidentes_agg_condicoes_via",
                "primary_keys": ["id"],
            },
            "agg_sazonalidade": {
                "fn": create_acidentes_agg_sazonalidade,
                "target": "acidentes_agg_sazonalidade",
                "primary_keys": ["id"],
            },
            "agg_trechos_criticos": {
                "fn": create_acidentes_agg_trechos_criticos,
                "target": "acidentes_agg_trechos_criticos",
                "primary_keys": ["id"],
            },
        },
    }
}
