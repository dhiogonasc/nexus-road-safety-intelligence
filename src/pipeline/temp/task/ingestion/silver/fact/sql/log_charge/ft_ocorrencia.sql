COPY (
    SELECT DISTINCT ano, uf
    FROM "silver"."ft_ocorrencia"
) 
TO '{log_path}/carga.parquet' (
    FORMAT PARQUET,
    OVERWRITE_OR_IGNORE 1
);