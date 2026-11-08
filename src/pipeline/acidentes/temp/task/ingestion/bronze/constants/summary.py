from pathlib import Path
from typing import List
from pydantic import BaseModel

from constants import SOURCE_OCORRENCIAS
from src.persistence.storage.provider import StorageProvider


class BronzeTable(BaseModel):
    name: str
    source: str

    @property
    def storage(self):
        base_path = Path("bronze").as_posix()
        return StorageProvider(
            table_name=self.name,
            base_path=base_path,
        )


raw_ocorrencias = BronzeTable(
    name="raw_ocorrencias",
    source=SOURCE_OCORRENCIAS,
)

TABLES: List[BronzeTable] = [raw_ocorrencias]
