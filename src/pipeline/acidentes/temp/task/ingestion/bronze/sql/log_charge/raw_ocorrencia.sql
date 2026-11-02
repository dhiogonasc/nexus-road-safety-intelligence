COPY (
    SELECT MAX(data_carga) as data_carga
    FROM "bronze"."raw_ocorrencia"
) 
TO '{log_path}/carga.parquet' (
    FORMAT PARQUET,
    OVERWRITE_OR_IGNORE 1
);