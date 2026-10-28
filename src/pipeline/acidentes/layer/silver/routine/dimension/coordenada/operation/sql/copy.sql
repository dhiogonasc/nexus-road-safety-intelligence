COPY "silver"."dim_coordenada"
TO '{storage_path}/dim_coordenada.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);