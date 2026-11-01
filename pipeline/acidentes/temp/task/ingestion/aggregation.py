from src.pipeline.acidentes.temp.ingestion.aggregation.staging import stg_tasks
from src.pipeline.acidentes.temp.ingestion.aggregation.aggregation import agg_tasks

staging_tasks = [
    stg_task.create_prefect_task() 
    for stg_task in stg_tasks
]

aggregation_tasks = [
    agg_task.create_prefect_task()
    for agg_task in agg_tasks
]

aggregate_tasks = [
    staging_tasks,
    aggregation_tasks
]
