COPY (
    SELECT DISTINCT ano, uf
    FROM "silver"."stg_ocorrencias"
) 
TO '{log_path}/carga.parquet' (
    FORMAT PARQUET,
    OVERWRITE_OR_IGNORE 1
);