from src.model.staging import StgOperations, StgTask
from .operation import (
    stage,
    copy_to_parquet,
    log_charge,
)

task = StgTask(
    label="ocorrencias",
    operations=StgOperations(
        stage=stage,
        copy_to_parquet=copy_to_parquet,
        log_charge=log_charge,
    ),
)
