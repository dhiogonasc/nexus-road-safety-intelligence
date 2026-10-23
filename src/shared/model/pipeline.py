from __future__ import annotations

from typing import Callable, Dict, List
from pydantic import BaseModel
from src.shared.model.entity import Table


class PipelineAsset(BaseModel):
    """Define estrutura de rotinas"""

    table: Table
    upsert_fn: Callable
    depends_on: List[PipelineAsset] = []


class DomainPipelineConfig(BaseModel):
    """Define estrutura da configuração de rotinas do domínio"""

    bronze: Dict[str, str]
    silver: List[PipelineAsset]
    gold: List[PipelineAsset]
    exportation: List[PipelineAsset]


class GlobalPipelineConfig(BaseModel):
    """Define estrutura da configuração de rotinas global"""

    domain_pipeline_configs: Dict[str, DomainPipelineConfig]
    
    def _validate_domain(self, domain: str) -> None:
        """Valida se o domínio existe nas configurações globais."""
        if domain not in self.domain_pipeline_configs:
            raise ValueError(
                f"Domínio '{domain}' não foi encontrado nas configurações globais."
            )
    
    def get_domain_config(self, domain: str) -> DomainPipelineConfig:
        """Retorna a configuração do pipeline de um domínio"""
        self._validate_domain(domain)
        return self.domain_pipeline_configs[domain]