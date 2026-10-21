"""src/pipeline/index.py"""

from constants import AC_OCORRENCIA_DIR
from src.pipeline.silver.acidentes.model import (
    dim_causa,
    dim_classificacao,
    dim_tipo,
    dim_condicao_metereologica,
    dim_coordenada,
)
from src.pipeline.silver.acidentes.transform import (
    upsert_acidentes_dim_causa,
    upsert_acidentes_dim_classificacao,
    upsert_acidentes_dim_tipo,
    upsert_acidentes_dim_condicao_metereologica,
    upsert_acidentes_dim_coordenada,
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
        },
        "gold": {},
    }
}
