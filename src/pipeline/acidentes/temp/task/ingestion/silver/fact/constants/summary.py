from typing import List

from pydantic import BaseModel

from ....silver.staging.constants.summary import (
    StagingTable,
    stg_ocorrencias,
)


class GoldTable(BaseModel):
    name: str
    source: StagingTable


ft_ocorrencia = GoldTable(
    name="ft_ocorrencia",
    source=stg_ocorrencias,
)

TABLES: List[GoldTable] = [
    ft_ocorrencia,
]
