from src.model.aggregation import AggOperations, AggTask
from .operation import (
    create,
    bootstrap,
    upsert,
    copy_to_parquet,
)

task = AggTask(
    label="letalidade_trechos_criticos",
    operations=AggOperations(
        create=create,
        bootstrap=bootstrap,
        upsert=upsert,
        copy_to_parquet=copy_to_parquet,
    ),
)
