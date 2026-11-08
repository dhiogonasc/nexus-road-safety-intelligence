from typing import List
from pydantic import BaseModel

from src.persistence.storage.provider import StorageProvider
from src.pipeline.acidentes.temp.task.ingestion.silver.dimension.constants.storage import (
    BASE_PATH as DIMENSION_PATH,
)
from src.pipeline.acidentes.temp.task.ingestion.silver.fact.constants.storage import (
    BASE_PATH as FACT_PATH,
)
from src.pipeline.acidentes.temp.task.ingestion.gold.constants.storage import BASE_PATH


class GoldSource(BaseModel):
    fact: StorageProvider
    dimension: List[StorageProvider]


class GoldTable(BaseModel):
    name: str
    storage: StorageProvider
    source: GoldSource

    @property
    def all_sources(self):
        return [
            self.source.fact,
            *self.source.dimension,
        ]


agg_categorizacao_local = GoldTable(
    name="agg_categorizacao_local",
    storage=StorageProvider(
        table_name="agg_categorizacao_local",
        base_path=BASE_PATH,
    ),
    source=GoldSource(
        fact=StorageProvider(
            table_name="ft_ocorrencia",
            base_path=FACT_PATH,
        ),
        dimension=[
            StorageProvider(
                table_name="dim_local",
                base_path=DIMENSION_PATH,
            ),
            StorageProvider(
                table_name="dim_categoria",
                base_path=DIMENSION_PATH,
            ),
        ],
    ),
)


TABLES = [
    agg_categorizacao_local,
]
