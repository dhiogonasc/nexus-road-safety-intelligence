"""src/pipeline/acidentes/index.py"""

from constants import AC_OCORRENCIA_DIR

from src.shared.model.pipeline import DomainPipelineConfig
from src.pipeline.acidentes.silver.index import config as silver_config
from src.pipeline.acidentes.gold.index import config as gold_config
from src.pipeline.acidentes.exportation.index import config as exportation_config

PIPELINE_CONFIG = DomainPipelineConfig(
    name="acidentes",
    raw={
        "ocorrencias": str(AC_OCORRENCIA_DIR / "*.csv"),
    },
    process={
        "silver": silver_config,
        "gold": gold_config,
        "exportation": exportation_config,
    },
)
