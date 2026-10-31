from src.model.fact import FtOperations, FtTask
from .operation import (
    create,
    bootstrap,
    upsert_by_partitions,
    copy_to_parquet,
)

task = FtTask(
    label="ocorrencia",
    operations=FtOperations(
        create=create,
        bootstrap=bootstrap,
        upsert_by_partitions=upsert_by_partitions,
        copy_to_parquet=copy_to_parquet,
    ),
)
