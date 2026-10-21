INSERT INTO "{table.schema}"."{table.name}" ({table.columns_name})
SELECT {table.columns_name}
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/{domain}/{table.schema}/{table.name}/*.parquet')
WHERE ({unique_columns}) NOT IN (SELECT {unique_columns} FROM "{stage_schema}"."{table_name}");