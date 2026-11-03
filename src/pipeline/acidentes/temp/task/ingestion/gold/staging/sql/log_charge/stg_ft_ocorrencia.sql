COPY (
    SELECT DISTINCT ano, uf
    FROM "gold"."stg_ft_ocorrencia"
) 
TO '{log_path}/carga.parquet' (
    FORMAT PARQUET,
    OVERWRITE_OR_IGNORE 1
);