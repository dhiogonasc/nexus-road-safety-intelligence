from typing import Optional

import duckdb


def execute_query(
    conn: duckdb.DuckDBPyConnection,
    query_dict: dict[str, str],
    query_key: str,
    **kwargs
) -> duckdb.DuckDBPyRelation:
    sql = query_dict[query_key]
    query = sql.format(**kwargs)
    return conn.execute(query)


def load_extensions(
    conn: duckdb.DuckDBPyConnection,
    extensions: str | list[str],
) -> None:
    if isinstance(extensions, str):
        extensions = [extensions]

    for extension in extensions:
        conn.execute(f"LOAD {extension};")


def attach_connections(
    conn: duckdb.DuckDBPyConnection,
    connections: list[dict[str, str]],
) -> None:
    for config in connections:
        conn_string = config["conn_string"]
        conn_alias = config["conn_alias"]
        conn_option = config.get("conn_option", "")

        conn.execute(
            f"ATTACH '{conn_string}' AS {conn_alias} {conn_option};"
        )


def create_schema(
    conn: duckdb.DuckDBPyConnection,
    schema: str,
    catalog: Optional[str] = None,
) -> None:
    sch = f'"{catalog}"."{schema}"' if catalog else f'"{schema}"'
    conn.execute(f"CREATE SCHEMA IF NOT EXISTS {sch};")
