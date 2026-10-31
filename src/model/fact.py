from typing import Callable, ContextManager, Optional

import duckdb

from prefect import Task, task
from pydantic import BaseModel, ConfigDict

from src.persistence.storage.settings import BucketSettings


class FtOperations(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    create: Task
    bootstrap: Task
    upsert_by_partitions: Task
    copy_to_parquet: Task


class FtTask(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    label: str
    operations: FtOperations

    def run(
        self,
        conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
        settings: Optional[BucketSettings] = None,
    ):
        operations = self.operations

        create_future = operations.create.submit(
            conn_fn=conn_fn,
            wait_for=[],
        )

        bootstrap_future = operations.bootstrap.submit(
            conn_fn=conn_fn,
            settings=settings,
            wait_for=[create_future],
        )

        upsert_future = operations.upsert_by_partitions.submit(
            conn_fn=conn_fn,
            wait_for=[bootstrap_future],
        )

        copy_future = operations.copy_to_parquet.submit(
            conn_fn=conn_fn,
            settings=settings,
            wait_for=[upsert_future],
        )

        copy_future.result()

    def create_prefect_task(self):
        @task(
            name=f"ft_{self.label}_clean_ingestion",
            task_run_name=f"ft_{self.label}_clean_ingestion",
        )
        def fact_task(
            conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
            settings: Optional[BucketSettings] = None,
        ):
            self.run(
                conn_fn=conn_fn,
                settings=settings,
            )

        return fact_task
