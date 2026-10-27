COPY "silver"."dim_localizacao"
TO '{storage_path}/dim_localizacao.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);