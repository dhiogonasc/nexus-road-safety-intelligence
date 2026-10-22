"""src/pipeline/index.py"""

from src.shared.model.pipeline import GlobalPipelineConfig
from src.pipeline.acidentes.index import PIPELINE_CONFIG as ACIDENTES_PIPELINE_CONFIG

PIPELINE_CONFIG = GlobalPipelineConfig(
    domain_pipeline_configs={
        "acidentes": ACIDENTES_PIPELINE_CONFIG,
    }
)
