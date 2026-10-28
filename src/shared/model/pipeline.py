from __future__ import annotations

from typing import Callable, Dict, List
from pydantic import BaseModel, model_validator


class Routine(BaseModel):
    """Define estrutura de rotinas"""
    label: str
    operations: List[Callable]
    depends_on: List[Routine] = []

class Layer(Routine):
    """Define estrutura de rotinas de camada"""
    routines: List[Routine]
    
class Catalog(Routine):
    """Define estrutura de rotinas de camada"""
    routines: List[Routine]


Routine.model_rebuild()
Layer.model_rebuild()


class DomainPipelineConfig(BaseModel):
    """Define estrutura da configuração de rotinas do domínio"""

    name: str
    raw: Dict[str, str]
    processes: Dict[str, LayerSchemaConfig]

    @model_validator(mode="after")
    def propagate_parent_properties(self) -> "DomainPipelineConfig":
        """Propaga o catalog para todas as configurações filhas."""
        for process in self.processes.values():
            if not process.catalog:
                process.catalog = self.name

        return self


DomainPipelineConfig.model_rebuild()


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
