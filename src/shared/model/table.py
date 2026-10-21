"""src/shared/model/table.py"""

from typing import List, Literal
from pydantic import BaseModel, computed_field, model_validator


class Column(BaseModel):
    """Define estrutura de colunas"""

    name: str
    data_type: str
    attribute: Literal["NULL", "NOT NULL"] = "NULL"
    identity: bool = False

    @model_validator(mode="after")
    def ensure_rules(self) -> "Column":
        """Verifica atributo associdado a identidade"""
        if self.identity:
            self.attribute = "NOT NULL"
        return self


class Table(BaseModel):
    """Define estrutura de tabelas"""

    schema: str
    name: str
    columns: List[Column]
    unique_constraint: List[str]

    @computed_field
    @property
    def columns_name(self) -> str:
        """Retorna os nomes das colunas como um campo computado."""
        return ",\n ".join([column.name for column in self.columns])

    @computed_field
    @property
    def unique_columns_name(self) -> str:
        """Retorna os nomes das colunas (unique constraint) como um campo computado."""
        return ",\n ".join([column for column in self.unique_constraint])

    @computed_field
    @property
    def columns_definition(self) -> str:
        """Gera automaticamente as definições DDL como um campo computado."""
        definitions = []

        for col in self.columns:
            definitions.append(f'"{col.name}" {col.data_type} {col.attribute}')

        return ",\n ".join(definitions)
