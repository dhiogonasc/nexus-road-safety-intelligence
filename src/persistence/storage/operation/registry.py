import uuid

import duckdb

from src.shared.system.file import load_module_queries
from src.persistence.database.operation import execute_query
from ..settings import BucketSettings

QUERIES = load_module_queries(current_file=__file__)


def create_bucket_secret(
    conn: duckdb.DuckDBConnection,
    settings: BucketSettings,
):
    suffix = uuid.uuid4().hex[:8]
    execute_query(
        conn=conn,
        query_key="create_bucket_secret",
        query_dict=QUERIES,
        settings=settings,
        suffix=suffix,
    )
