from src.shared.system.file import load_module
from .. import sql

SHARED_QUERIES_SQL = load_module(module=sql)
