COPY "silver"."dim_tipo" 
TO '{storage_path}/dim_tipo.parquet'
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);