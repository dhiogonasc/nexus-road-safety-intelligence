import duckdb


def _create_target_table(
    conn: duckdb.DuckDBPyConnection,
    source_schema: str,
    source_table: str,
    full_target: str,
    primary_keys: list[str],
) -> list[str]:
    columns_info = conn.execute(f"""
        SELECT 
            column_name, 
            data_type 
        FROM information_schema.columns 
        WHERE table_schema = '{source_schema}' 
          AND table_name = '{source_table}'
        ORDER BY ordinal_position;
    """).fetchall()

    if not columns_info:
        raise ValueError(
            f"A tabela origem '{source_schema}.{source_table}' não foi encontrada."
        )

    column_names = [col[0] for col in columns_info]

    ddl_columns = [f"{col[0]} {col[1]}" for col in columns_info]
    pk_str = ", ".join(primary_keys)
    ddl_columns.append(f"PRIMARY KEY ({pk_str})")
    ddl_body = ",\n            ".join(ddl_columns)

    create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {full_target} (
            {ddl_body}
        );
    """
    conn.execute(create_table_sql)

    return column_names


def _upsert_target_table(
    conn: duckdb.DuckDBPyConnection,
    full_source: str,
    full_target: str,
    column_names: list[str],
    primary_keys: list[str],
) -> None:
    cols_str = ", ".join(column_names)
    conflict_str = ", ".join(primary_keys)

    update_cols = [col for col in column_names if col not in primary_keys]
    update_str = ",\n            ".join(
        [f"{col} = EXCLUDED.{col}" for col in update_cols]
    )

    upsert_sql = f"""
        INSERT INTO {full_target} (
            {cols_str}
        )
        SELECT
            {cols_str}
        FROM {full_source}
        ON CONFLICT ({conflict_str}) 
        DO UPDATE SET
            {update_str};
    """
    conn.execute(upsert_sql)


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
