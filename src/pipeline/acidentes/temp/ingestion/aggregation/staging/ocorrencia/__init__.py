from src.model.staging import StgOperations, StgTask
from .operation import stage

task = StgTask(
    label="ft_ocorrencia",
    operations=StgOperations(stage=stage),
)
