COPY "silver"."dim_local"
TO '{storage_path}/dim_local.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);