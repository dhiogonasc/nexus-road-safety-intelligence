COPY "silver"."dim_categoria"
TO '{storage_path}/dim_categoria.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);