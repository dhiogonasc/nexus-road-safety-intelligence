COPY "silver"."ft_ocorrencia"
TO '{storage_path}/ft_ocorrencia.parquet'
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);