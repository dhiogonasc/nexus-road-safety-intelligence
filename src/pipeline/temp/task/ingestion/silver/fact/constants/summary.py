from pathlib import Path
from typing import List

from pydantic import BaseModel

from src.persistence.storage.provider import StorageProvider

from ...dimension.constants.summary import (
    STG_OCORRENCIAS_STORAGE,
    ocorrencia_dimension,
)


class SilveFactTable(BaseModel):
    name: str
    staging: StorageProvider
    dimension: List[StorageProvider]

    @property
    def storage(self):
        base_path = Path(
            "silver",
            "fact",
        ).as_posix()
        return StorageProvider(
            table_name=self.name,
            base_path=base_path,
        )

    @property
    def all_sources(self):
        return [
            self.staging,
            *self.dimension,
        ]


ft_ocorrencia = SilveFactTable(
    name="ft_ocorrencia",
    staging=STG_OCORRENCIAS_STORAGE,
    dimension=[table.storage for table in ocorrencia_dimension],
)

TABLES: List[SilveFactTable] = [ft_ocorrencia]
