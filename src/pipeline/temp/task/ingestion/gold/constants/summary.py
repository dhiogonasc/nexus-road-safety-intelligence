from pathlib import Path
from typing import List
from pydantic import BaseModel

from src.persistence.storage.provider import StorageProvider
from ...silver.fact.constants.summary import ft_ocorrencia
from ...silver.dimension.constants.summary import dim_local, dim_categoria


class GoldTable(BaseModel):
    name: str
    fact: StorageProvider
    dimension: List[StorageProvider]

    @property
    def storage(self):
        base_path = Path("gold").as_posix()
        return StorageProvider(
            table_name=self.name,
            base_path=base_path,
        )

    @property
    def all_sources(self):
        return [
            self.fact,
            *self.dimension,
        ]


agg_categorizacao_local = GoldTable(
    name="agg_categorizacao_local",
    fact=ft_ocorrencia.storage,
    dimension=[
        dim_local.storage,
        dim_categoria.storage,
    ],
)


TABLES: List[GoldTable] = [agg_categorizacao_local]
