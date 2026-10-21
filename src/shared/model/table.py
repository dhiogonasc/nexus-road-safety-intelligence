from typing import List, Literal
from pydantic import BaseModel, model_validator

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
    
    def get_columns(self) -> List[str]:
        """Retorna uma lista com apenas os nomes das colunas."""
        return [col.name for col in self.columns]

    def get_definitions(self) -> List[str]:
        """Retorna a lista de strings com as definições DDL das colunas e constraints."""
        definitions = []
        
        for col in self.columns:
            definitions.append(f'{col.name} {col.data_type} {col.attribute}')
            
        for constraint in self.unique_constraints:
            cols_str = ", ".join([f'"{c}"' for c in constraint])
            definitions.append(f"UNIQUE ({cols_str})")
            
        return definitions