COPY (
    SELECT DISTINCT data_carga
    FROM "bronze"."raw_ocorrencias"
) 
TO '{log_path}/carga.parquet' (
    FORMAT PARQUET,
    OVERWRITE_OR_IGNORE 1
);