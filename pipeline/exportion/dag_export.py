"""pipeline/stage/gold.py"""

from functools import partial
from prefect import flow

from settings import bucket_settings
from src.shared.utils.fn import named_partial
from src.pipeline.index import PIPELINE_CONFIG
from src.shared.pipeline.task import (
    task_create_schema,
    task_create_table,
    task_open_bucket_operation,
)
from src.shared.db.connection import create_connection
from src.shared.db.operation import (
    bootstrap_table,
    copy_table_to_parquet,
    create_table,
)


@flow(
    name="Exportation",
    flow_run_name="flow_gold: {domain}",
)
def flow_exportation(
    database: str,
    domain: str,
) -> None:
    """Orquestra a exportacao de um dominio para postgres"""
    pass