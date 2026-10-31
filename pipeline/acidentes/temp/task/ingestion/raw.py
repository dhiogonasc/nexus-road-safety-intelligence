from src.pipeline.acidentes.temp.ingestion.raw import r_tasks

raw_tasks = [
    r_task.create_prefect_task() 
    for r_task in r_tasks
]