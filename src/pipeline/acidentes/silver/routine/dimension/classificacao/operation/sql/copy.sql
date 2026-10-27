COPY "silver"."dim_classificacao"
TO '{storage_path}/dim_classificacao.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);