from .operation import process_routine as routine_processor

routine = {
    "label": "stg",
    "processor": routine_processor,
    "depends_on": [],
}
