import duckdb

from src.shared.db.operation import execute_query
from src.shared.system.file import load_module_queries

QUERIES = load_module_queries(current_file=__file__)


def _fetch_columns_info(
    conn: duckdb.DuckDBPyConnection,
    source_schema: str,
    source_table: str,
):
    return execute_query(
        conn=conn,
        query_key="fetch_columns_info",
        query_dict=QUERIES,
        source_schema=source_schema,
        source_table=source_table,
    )


def _create_table_from_ddl_body(
    conn: duckdb.DuckDBPyConnection,
    full_target: str,
    ddl_body: str,
):
    execute_query(
        conn=conn,
        query_key="create_table_from_ddl_body",
        query_dict=QUERIES,
        full_target=full_target,
        ddl_body=ddl_body,
    )


def _upsert(
    conn: duckdb.DuckDBPyConnection,
    full_target: str,
    full_source: str,
    cols_str: str,
    conflict_str: str,
    update_str: str,
):
    execute_query(
        conn=conn,
        query_key="upsert",
        query_dict=QUERIES,
        full_target=full_target,
        full_source=full_source,
        cols_str=cols_str,
        conflict_str=conflict_str,
        update_str=update_str,
    )


def _create_target_table(
    conn: duckdb.DuckDBPyConnection,
    source_schema: str,
    source_table: str,
    full_target: str,
    primary_keys: list[str],
) -> list[str]:

    columns_info = _fetch_columns_info(
        conn=conn,
        source_schema=source_schema,
        source_table=source_table,
    ).fetchall()

    ddl_columns = [f"{col[0]} {col[1]}" for col in columns_info]
    pk_str = ", ".join(primary_keys)
    ddl_columns.append(f"PRIMARY KEY ({pk_str})")
    ddl_body = ",\n".join(ddl_columns)

    _create_table_from_ddl_body(
        conn=conn,
        full_target=full_target,
        ddl_body=ddl_body,
    )

    return [col[0] for col in columns_info]


def _upsert_target_table(
    conn: duckdb.DuckDBPyConnection,
    full_source: str,
    full_target: str,
    column_names: list[str],
    primary_keys: list[str],
) -> None:
    update_cols = [col for col in column_names if col not in primary_keys]
    update_str = ",\n ".join([f"{col} = EXCLUDED.{col}" for col in update_cols])
    cols_str = ", ".join(column_names)
    conflict_str = ", ".join(primary_keys)

    _upsert(
        conn=conn,
        full_target=full_target,
        full_source=full_source,
        cols_str=cols_str,
        conflict_str=conflict_str,
        update_str=update_str,
    )


def export_aggregation(
    conn: duckdb.DuckDBPyConnection,
    source_schema: str,
    source_table: str,
    target_catalog: str,
    target_schema: str,
    target_table: str,
    primary_keys: list[str],
) -> None:
    full_source = f'"{source_schema}"."{source_table}"'
    full_target = f"{target_catalog}.{target_schema}.{target_table}"

    column_names = _create_target_table(
        conn=conn,
        source_schema=source_schema,
        source_table=source_table,
        full_target=full_target,
        primary_keys=primary_keys,
    )

    _upsert_target_table(
        conn=conn,
        full_source=full_source,
        full_target=full_target,
        column_names=column_names,
        primary_keys=primary_keys,
    )
