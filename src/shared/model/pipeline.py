from __future__ import annotations

from typing import Callable, Dict, List
from pydantic import BaseModel, model_validator


class Routine(BaseModel):
    """Define estrutura de rotinas"""

    label: str
    operations: List[Callable]
    depends_on: List[Routine] = []


class Layer(BaseModel):
    """Define estrutura de rotinas de camada"""

    label: str
    routines: List[Routine]
    operations: List[Callable] = []
    depends_on: List[Layer] = []
    required_extensions: List[str] = []


class Catalog(BaseModel):
    """Define estrutura de rotinas de catalogo"""

    label: str
    layers: List[Layer]

Routine.model_rebuild()
Layer.model_rebuild()
