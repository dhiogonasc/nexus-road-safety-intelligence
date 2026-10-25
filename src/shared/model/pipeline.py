from __future__ import annotations

from typing import Callable, Dict, List, Optional
from pydantic import BaseModel, computed_field, model_validator
from src.shared.model.entity import Table


class PipelineAsset(BaseModel):
    """Define estrutura de rotinas"""

    table: Table
    upsert_fn: Callable
    depends_on: List[PipelineAsset] = []


PipelineAsset.model_rebuild()


class LayerSchemaConfig(BaseModel):
    catalog: Optional[str] = None
    name: str
    assets: List[PipelineAsset]

    @computed_field
    @property
    def fqn(self) -> str:
        """Retorna o nome totalmente qualificado do schema (FQN)."""
        if self.catalog:
            return f'"{self.catalog}"."{self.name}"'
        return f'"{self.name}"'

    @model_validator(mode="after")
    def propagate_parent_properties(self) -> "LayerSchemaConfig":
        """Propaga o catalog e o nome do schema para todas as tabelas filhas."""
        for asset in self.assets:
            asset.table.schema = self.name
            if self.catalog and not asset.table.catalog:
                asset.table.catalog = self.catalog

        return self


LayerSchemaConfig.model_rebuild()


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
