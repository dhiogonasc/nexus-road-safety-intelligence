COPY "bronze"."raw_ocorrencias" 
TO '{storage_path}/' (
    FORMAT PARQUET,
    PARTITION_BY (data_carga),
    OVERWRITE_OR_IGNORE 1
);