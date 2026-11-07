import duckdb
from pydantic import BaseModel, Field

from .connector import DuckDBConnector


class DuckDBProvider(BaseModel):
    connector: DuckDBConnector = Field(default_factory=DuckDBConnector)

    def execute_query(self, sql: str, **kwargs) -> duckdb.DuckDBPyRelation:
        with self.connector.create_connection() as conn:
            return conn.execute(query=sql.format(**kwargs))
