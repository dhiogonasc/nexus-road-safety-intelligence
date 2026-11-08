COPY (
    SELECT MAX(data_carga) as data_carga
    FROM "raw_ocorrencias"
) 
TO '{log_path}/carga.parquet' (
    FORMAT PARQUET,
    OVERWRITE_OR_IGNORE 1
);