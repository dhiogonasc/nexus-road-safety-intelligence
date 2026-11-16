from typing import List, Optional, Union
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
    base_path: str = Field(..., exclude=True)
    source: Union[str, TableSource]

    @property
    def storage(self):
        return StorageProvider(
            table_name=self.name,
            base_path=self.base_path,
        )


class RawTable(BaseTable):
    base_path: str = Field(
        default=RAW_BASE_PATH,
        exclude=True,
    )
    source: str


class StagingTable(BaseTable):
    base_path: str = Field(
        default=STG_BASE_PATH,
        exclude=True,
    )


class DimensionTable(BaseTable):
    base_path: str = Field(
        default=DIM_BASE_PATH,
        exclude=True,
    )


class FactTable(BaseTable):
    base_path: str = Field(
        default=FCT_BASE_PATH,
        exclude=True,
    )


class AggregationTable(BaseTable):
    base_path: str = Field(
        default=AGG_BASE_PATH,
        exclude=True,
    )
