COPY "silver"."dim_clima"
TO '{storage_path}/dim_clima.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);