from pathlib import Path

import duckdb

from constants import DB_DIR

conn = duckdb.connect()

storage_path = Path(
    DB_DIR,
    "acidentes",
    "silver",
    "staging",
    "ocorrencia",
)
query = f"""
    SELECT *
    FROM read_parquet('/{storage_path}/**/*.parquet', filename = true);
"""

df = conn.execute(query).fetchdf()
print(df)
