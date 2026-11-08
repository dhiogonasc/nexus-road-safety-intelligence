from pathlib import Path
from typing import List
from pydantic import BaseModel

from ....bronze.constants.summary import raw_ocorrencias
from src.persistence.storage.provider import StorageProvider


class SilverStagingTable(BaseModel):
    name: str
    source: StorageProvider

    @property
    def storage(self):
        base_path = Path(
            "silver",
            "staging",
        ).as_posix()
        return StorageProvider(
            table_name=self.name,
            base_path=base_path,
        )


stg_ocorrencias = SilverStagingTable(
    name="stg_ocorrencias",
    source=raw_ocorrencias.storage,
)

TABLES: List[SilverStagingTable] = [stg_ocorrencias]
