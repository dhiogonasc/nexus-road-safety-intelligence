from src.pipeline.acidentes.temp.ingestion.clean.staging import stg_tasks
from src.pipeline.acidentes.temp.ingestion.clean.dimension import dim_tasks
from src.pipeline.acidentes.temp.ingestion.clean.fact import ft_tasks

staging_tasks = [
    stg_task.create_prefect_task() 
    for stg_task in stg_tasks
]
dimension_tasks = [
    dim_task.create_prefect_task() 
    for dim_task in dim_tasks
]
fact_tasks = [
    ft_task.create_prefect_task() 
    for ft_task in ft_tasks
]

clean_tasks = [
    staging_tasks, 
    dimension_tasks, 
    fact_tasks,
]