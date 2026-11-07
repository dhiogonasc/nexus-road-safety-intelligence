from pathlib import Path
from typing import List

from pydantic import BaseModel

from constants import OCORRENCIAS_DIR


class BronzeTable(BaseModel):
    name: str
    source_data_path: str


raw_ocorrencias = BronzeTable(
    name="raw_ocorrencias",
    source_data_path=Path(OCORRENCIAS_DIR, "*.csv").as_posix(),
)

TABLES: List[BronzeTable] = [
    raw_ocorrencias,
]
