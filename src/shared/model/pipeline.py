from typing import Callable, Dict, List
from pydantic import BaseModel
from src.shared.model.entity import Table


class PipelineAsset(BaseModel):
    """Define estrutura de rotinas"""

    table: Table
    upsert_fn: Callable
    depends_on: List["PipelineAsset"] = []


class DomainPipelineConfig(BaseModel):
    """Define estrutura da configuração de rotinas para um domínio"""

    bronze: Dict[str, str]
    silver: List[PipelineAsset]
    gold: List[PipelineAsset]


class GlobalPipelineConfig(BaseModel):
    """Define estrutura da configuração de rotinas global"""

    domain_pipeline_configs: Dict[str, DomainPipelineConfig]

    def get_domain_pipeline_config(self, domain: str) -> DomainPipelineConfig:
        """Retorna a configuração de rotina para um domínio específico."""
        if domain not in self.domain_pipeline_configs:
            raise ValueError(
                f"Domínio '{domain}' não foi encontrado nas configurações globais."
            )

        return self.domain_pipeline_configs[domain]
