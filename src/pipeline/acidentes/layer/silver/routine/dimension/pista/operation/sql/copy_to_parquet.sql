COPY "silver"."dim_pista"
TO '{storage_path}/dim_pista.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);