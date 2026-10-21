COPY "silver"."dim_causa" 
TO 's3://{settings.STORAGE_BUCKET}/{domain}/silver/dim_causa/' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);