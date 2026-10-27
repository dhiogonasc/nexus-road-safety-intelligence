COPY "silver"."dim_causa"
TO '{storage_path}/dim_causa.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);