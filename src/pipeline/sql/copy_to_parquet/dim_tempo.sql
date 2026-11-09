COPY "silver"."dim_tempo"
TO '{storage_path}/dim_tempo.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);