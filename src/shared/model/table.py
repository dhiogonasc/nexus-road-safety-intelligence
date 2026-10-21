from typing import List, Literal
from pydantic import BaseModel, computed_field, model_validator

class Column(BaseModel):
    name: str
    data_type: str
    attribute: Literal["NULL", "NOT NULL", "GENERATED ALWAYS AS IDENTITY"] = "NULL"
    identity: bool = False
    
    @model_validator(mode="after")
    def ensure_rules(self) -> "Column":
        if self.identity:
            self.attribute = "GENERATED ALWAYS AS IDENTITY"
        return self
    
class Table(BaseModel):
    schema: str
    name: str
    columns: List[Column]
    unique_constraints: List[List[str]] = []
    
    @computed_field
    @property
    def columns_name(self) -> str:
        """Retorna os nomes das colunas como um campo computado."""
        return ",\n ".join([col.name for col in self.columns])

    @computed_field
    @property
    def columns_definition(self) -> str:
        """Gera automaticamente as definições DDL como um campo computado."""
        definitions = []
        
        for col in self.columns:
            definitions.append(f'"{col.name}" {col.data_type} {col.attribute}')
            
        for constraint in self.unique_constraints:
            cols_str = ", ".join([f'"{c}"' for c in constraint])
            constraint_name = f"" + "_".join(constraint)
            definitions.append(f"CONSTRAINT {constraint_name} UNIQUE ({cols_str})")
            
        return ",\n ".join(definitions)