from typing import List

from constants import SOURCE_OCORRENCIAS
from .schema import (
    BaseTable,
    TableSource,
    RawTable,
    StagingTable,
    DimensionTable,
    FactTable,
    AggregationTable,
)

raw_ocorrencias = RawTable(
    name="raw_ocorrencias",
    source=SOURCE_OCORRENCIAS,
)

stg_ocorrencias = StagingTable(
    name="stg_ocorrencias",
    source=TableSource(base=raw_ocorrencias.storage),
)

dim_categoria = DimensionTable(
    name="dim_categoria",
    source=TableSource(base=stg_ocorrencias.storage),
)
dim_clima = DimensionTable(
    name="dim_clima",
    source=TableSource(base=stg_ocorrencias.storage),
)
dim_local = DimensionTable(
    name="dim_local",
    source=TableSource(base=stg_ocorrencias.storage),
)
dim_tempo = DimensionTable(
    name="dim_tempo",
    source=TableSource(base=stg_ocorrencias.storage),
)

OCORRENCIA_DIM_LAYER: List[DimensionTable] = [
    dim_categoria,
    dim_clima,
    dim_local,
    dim_tempo,
]

fct_ocorrencia = FactTable(
    name="fct_ocorrencia",
    source=TableSource(
        base=stg_ocorrencias.storage,
        context=[table.storage for table in OCORRENCIA_DIM_LAYER],
    ),
)

agg_categorizacao_local = AggregationTable(
    name="agg_categorizacao_local",
    source=TableSource(
        base=fct_ocorrencia.storage,
        context=[
            dim_categoria.storage,
            dim_local.storage,
        ],
    ),
)

SCHEMAS: List[str] = [
    "bronze",
    "silver",
    "gold",
]

RAW_TABLES: List[RawTable] = [
    raw_ocorrencias,
]
STG_TABLES: List[StagingTable] = [
    stg_ocorrencias,
]
DIM_TABLES: List[DimensionTable] = [
    dim_categoria,
    dim_clima,
    dim_local,
    dim_tempo,
]
FCT_TABLES: List[FactTable] = [
    fct_ocorrencia,
]
AGG_TABLES: List[AggregationTable] = [
    agg_categorizacao_local,
]

ALL_TABLES: List[BaseTable] = [
    *DIM_TABLES,
    *FCT_TABLES,
    *AGG_TABLES,
]
