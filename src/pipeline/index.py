"""src/pipeline/index.py"""

from constants import AC_OCORRENCIA_DIR
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

PIPELINE_CONFIG = {
    "acidentes": {
        "bronze": {
            "ocorrencias": str(AC_OCORRENCIA_DIR / "*.csv"),
        },
        "silver": {
            "dim_causa": {
                "table": dim_causa,
                "upsert_fn": upsert_acidentes_dim_causa,
                "depends_on": [],
            },
            "dim_tipo": {
                "table": dim_tipo,
                "upsert_fn": upsert_acidentes_dim_tipo,
                "depends_on": [],
            },
            "dim_classificacao": {
                "table": dim_classificacao,
                "upsert_fn": upsert_acidentes_dim_classificacao,
                "depends_on": [],
            },
            "dim_condicao_metereologica": {
                "table": dim_condicao_metereologica,
                "upsert_fn": upsert_acidentes_dim_condicao_metereologica,
                "depends_on": [],
            },
            "dim_coordenada": {
                "table": dim_coordenada,
                "upsert_fn": upsert_acidentes_dim_coordenada,
                "depends_on": [],
            },
            "dim_tempo": {
                "table": dim_tempo,
                "upsert_fn": upsert_acidentes_dim_tempo,
                "depends_on": [],
            },
            "dim_pista": {
                "table": dim_pista,
                "upsert_fn": upsert_acidentes_dim_pista,
                "depends_on": [],
            },
            "dim_localizacao": {
                "table": dim_localizacao,
                "upsert_fn": upsert_acidentes_dim_localizacao,
                "depends_on": [],
            },
            "fato_ocorrencia": {
                "table": fato_ocorrencia,
                "upsert_fn": upsert_acidentes_fato_ocorrencia,
                "depends_on": [
                    "dim_causa",
                    "dim_tipo",
                    "dim_classificacao",
                    "dim_condicao_metereologica",
                    "dim_coordenada",
                    "dim_tempo",
                    "dim_pista",
                    "dim_localizacao",
                ],
            },
        },
        "gold": {},
    }
}
