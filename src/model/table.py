from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Union

from src.persistence.storage import StorageProvider

RAW_BASE_PATH = Path("raw").as_posix()
STG_BASE_PATH = Path("stg").as_posix()
DIM_BASE_PATH = Path("dim").as_posix()
FCT_BASE_PATH = Path("fct").as_posix()
AGG_BASE_PATH = Path("agg").as_posix()


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
