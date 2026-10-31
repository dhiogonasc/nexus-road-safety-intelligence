from src.model.dimension import DimOperations, DimTask
from .operation import (
    create,
    bootstrap,
    upsert,
    copy_to_parquet,
)

task = DimTask(
    label="clima",
    operations=DimOperations(
        create=create,
        bootstrap=bootstrap,
        upsert=upsert,
        copy_to_parquet=copy_to_parquet,
    ),
)
