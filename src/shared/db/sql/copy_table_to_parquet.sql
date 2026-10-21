COPY "{stage_schema}"."{table_name}"
TO 's3://{settings.STORAGE_BUCKET}/{domain}/{stage_schema}/{table_name}/' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);