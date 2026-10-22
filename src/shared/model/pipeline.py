"""src/shared/model/pipeline.py"""

from typing import Callable, List

from pydantic import BaseModel

from src.shared.model.entity import Table


class Asset(BaseModel):
    """Define estrutura de rotinas"""

    table: Table
    upsert_fn: Callable
    depends_on: List[Asset] = []
