COPY "silver"."dim_jurisdicao"
TO '{storage_path}/dim_jurisdicao.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);