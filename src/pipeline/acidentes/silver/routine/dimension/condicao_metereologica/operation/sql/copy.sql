COPY "silver"."dim_condicao_metereologica"
TO '{storage_path}/dim_condicao_metereologica.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);