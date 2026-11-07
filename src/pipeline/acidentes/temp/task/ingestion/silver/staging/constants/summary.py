from pathlib import Path
from typing import List

from pydantic import BaseModel

from src.pipeline.acidentes.temp.task.ingestion.bronze.constants.summary import (
    BronzeTable,
    raw_ocorrencias,
)


class StagingTable(BaseModel):
    name: str
    source: BronzeTable


stg_ocorrencias = StagingTable(
    name="stg_ocorrencias",
    source=raw_ocorrencias,
)

TABLES: List[StagingTable] = [
    stg_ocorrencias,
]
