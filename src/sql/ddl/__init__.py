from src.shared.file import load_module

from . import schema, table

SCHEMA_SQL = load_module(module=schema)
TABLE_SQL = load_module(module=table)
