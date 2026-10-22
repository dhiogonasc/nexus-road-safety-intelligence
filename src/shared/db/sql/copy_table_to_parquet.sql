COPY "{table.schema}"."{table.name}" 
TO 's3://{settings.STORAGE_BUCKET}/{domain}/{table.schema}/{table.name}/{table.name}.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);