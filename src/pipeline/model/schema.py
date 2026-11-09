from typing import List, Optional
from pydantic import BaseModel, Field

from src.persistence.storage.provider import StorageProvider
from .path import (
    AGG_BASE_PATH,
    DIM_BASE_PATH,
    FCT_BASE_PATH,
    RAW_BASE_PATH,
    STG_BASE_PATH,
)


class TableSource(BaseModel):
    base: StorageProvider
    context: Optional[List[StorageProvider]] = None

    @property
    def all(self):
        return [self.base, *(self.context or [])]


class BaseTable(BaseModel):
    name: str
    _base_path: str = Field(..., exclude=True)
    source: TableSource

    @property
    def storage(self):
        return StorageProvider(
            table_name=self.name,
            base_path=self._base_path,
        )


class RawTable(BaseTable):
    _base_path = RAW_BASE_PATH
    source: str

class StagingTable(BaseTable):
    _base_path = STG_BASE_PATH


class DimensionTable(BaseTable):
    _base_path = DIM_BASE_PATH


class FactTable(BaseTable):
    _base_path = FCT_BASE_PATH


class AggregationTable(BaseTable):
    _base_path = AGG_BASE_PATH
