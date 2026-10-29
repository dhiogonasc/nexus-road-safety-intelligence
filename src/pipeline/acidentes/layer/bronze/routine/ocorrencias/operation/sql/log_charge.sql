COPY (
    SELECT DISTINCT data_carga
    FROM read_parquet('{storage_path}/**/*.parquet', union_by_name = true)
) 
TO '{log_path}/carga.parquet' (
    FORMAT PARQUET,
    OVERWRITE_OR_IGNORE 1
);