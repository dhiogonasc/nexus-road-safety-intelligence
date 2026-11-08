from pathlib import Path
from typing import List

from pydantic import BaseModel

from ...staging.constants.summary import stg_ocorrencias
from src.persistence.storage.provider import StorageProvider


class SilverDimensionTable(BaseModel):
    name: str
    source: StorageProvider

    @property
    def storage(self):
        base_path = Path(
            "silver",
            "dimension",
        ).as_posix()
        return StorageProvider(
            table_name=self.name,
            base_path=base_path,
        )


STG_OCORRENCIAS_STORAGE = stg_ocorrencias.storage

dim_categoria = SilverDimensionTable(
    name="dim_categoria",
    source=STG_OCORRENCIAS_STORAGE,
)
dim_clima = SilverDimensionTable(
    name="dim_clima",
    source=STG_OCORRENCIAS_STORAGE,
)
dim_local = SilverDimensionTable(
    name="dim_local",
    source=STG_OCORRENCIAS_STORAGE,
)
dim_tempo = SilverDimensionTable(
    name="dim_tempo",
    source=STG_OCORRENCIAS_STORAGE,
)

ocorrencia_dimension: List[SilverDimensionTable] = [
    dim_categoria,
    dim_clima,
    dim_local,
    dim_tempo,
]

TABLES: List[SilverDimensionTable] = ocorrencia_dimension
