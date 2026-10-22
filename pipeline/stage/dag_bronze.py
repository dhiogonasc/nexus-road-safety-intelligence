"""pipeline/stage/dag_bronze.py"""

from functools import partial
from prefect import flow

from config import settings, bucket_settings
from src.shared.utils.fn import named_partial
from src.shared.db.operation import load_extensions
from src.shared.system.cmd import declare_domain
from src.shared.db.connection import create_connection
from src.pipeline.index import PIPELINE_CONFIG
from src.pipeline.acidentes.bronze.operation import copy_raw_to_parquet
from src.shared.pipeline.task import task_open_bucket_operation


@flow(
    name="Bronze",
    flow_run_name="flow_bronze: {domain}",
)
def flow_bronze(
    database: str,
    domain: str,
) -> None:
    """Orquestra o processamento bronze para um dominio e banco duckdb dedicado"""

    domain_pipeline_config = PIPELINE_CONFIG.get_domain_pipeline_config(domain=domain)
    bronze_tables = domain_pipeline_config.bronze

    load_extension = partial(
        load_extensions,
        extensions=[
            "httpfs",
            "parquet",
        ],
    )
    conn_fn = partial(
        create_connection,
        load_extensions_fn=load_extension,
        database=database,
    )

    futures = []
    for table_name, data_path in bronze_tables.items():
        future = task_open_bucket_operation.submit(
            conn_fn=conn_fn,
            settings=bucket_settings,
            bucket_operation_fn=named_partial(
                name=f"copy_{table_name}_to_parquet",
                fn=copy_raw_to_parquet,
                domain=domain,
                table_name=table_name,
                csv_path=data_path,
            ),
            secret_label=table_name,
        )
        futures.append(future)

    for future in futures:
        future.result()


if __name__ == "__main__":
    args = declare_domain()

    DOMAIN = args.domain
    DATABASE = settings.domain_db_path(domain=DOMAIN)

    flow_bronze(
        database=DATABASE,
        domain=DOMAIN,
    )
