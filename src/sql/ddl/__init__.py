from src.shared.system.file import load_module

from ...pipeline.sql.ddl import schema, table

SCHEMA_SQL = load_module(module=schema)
TABLE_SQL = load_module(module=table)
