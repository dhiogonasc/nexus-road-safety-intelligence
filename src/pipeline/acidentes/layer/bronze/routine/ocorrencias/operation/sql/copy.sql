COPY "bronze"."ocorrencias" 
TO '{storage_path}/' (
    FORMAT PARQUET,
    PARTITION_BY (data_carga, arquivo_fonte),
    OVERWRITE_OR_IGNORE 1
);