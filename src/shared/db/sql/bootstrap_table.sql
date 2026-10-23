INSERT INTO {table.fqn} ({table.columns_name})
SELECT {table.columns_name}
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/{domain}/{table.schema}/{table.name}/*.parquet')
WHERE ({table.unique_columns_name}) NOT IN (SELECT {table.unique_columns_name} FROM "{table.schema}"."{table.name}");