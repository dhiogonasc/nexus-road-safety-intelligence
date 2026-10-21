INSERT INTO "{stage_schema}"."{table_name}" ({columns})
SELECT {columns}
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/{domain}/{stage_schema}/{table_name}/*.parquet')
WHERE ({unique_columns}) NOT IN (SELECT {unique_columns} FROM "{stage_schema}"."{table_name}");