from functools import partial
from pathlib import Path
from typing import Optional

import duckdb

from src.persistence.storage import BucketSettings
from src.persistence.storage.utils import set_path
from src.persistence.database.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)

BASE_STORAGE_PATH = Path(
    "acidentes",
    "bronze",
    "ocorrencias",
)
set_storage_path = partial(
    set_path,
    base_path=BASE_STORAGE_PATH,
)

BASE_LOG_PATH = Path(
    "acidentes",
    "bronze",
    "log",
    "ocorrencias",
)

set_log_path = partial(
    set_path,
    base_path=BASE_LOG_PATH,
)


def create_table(
    conn: duckdb.DuckDBPyConnection,
    settings: Optional[BucketSettings] = None,
):
    """Delega a execução do script create_table.sql"""

    execute_query(
        conn=conn,
        query_key="create_table",
        query_dict=QUERIES,
        storage_path=set_storage_path(settings=settings),
        log_path=set_log_path(settings=settings),
    )
