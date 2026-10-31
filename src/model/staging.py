from typing import Callable, ContextManager, Optional

import duckdb

from prefect import Task, task
from pydantic import BaseModel, ConfigDict

from src.persistence.storage.settings import BucketSettings


class StgOperations(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    stage: Task
    copy_to_parquet: Task
    log_charge: Task


class StgTask(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    label: str
    operations: StgOperations

    def run(
        self,
        conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
        settings: Optional[BucketSettings] = None,
    ):
        operations = self.operations

        stage_future = operations.stage.submit(conn_fn=conn_fn)

        storage_futures = []
        copy_future = operations.copy_to_parquet.submit(
            conn_fn=conn_fn,
            settings=settings,
            wait_for=[stage_future],
        )
        storage_futures.append(copy_future)

        log_future = operations.log_charge.submit(
            conn_fn=conn_fn,
            settings=settings,
            wait_for=[stage_future],
        )
        storage_futures.append(log_future)

        for future in storage_futures:
            future.result()


    def create_prefect_task(self):
        @task(
            name=f"stg_{self.label}_clean_ingestion",
            task_run_name=f"stg_{self.label}_clean_ingestion",
        )
        def staging_task(
            conn_fn: Callable[[], ContextManager[duckdb.DuckDBPyConnection]],
            settings: Optional[BucketSettings] = None,
        ):
            self.run(
                conn_fn=conn_fn,
                settings=settings,
            )

        return staging_task
