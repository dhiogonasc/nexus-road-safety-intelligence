COPY (
    SELECT DISTINCT
        data_carga,
        arquivo_fonte
    FROM read_parquet('s3://{settings.STORAGE_BUCKET}/{domain}/bronze/{table_name}/**/*.parquet', union_by_name = true)
) 
TO 's3://{settings.STORAGE_BUCKET}/{domain}/bronze/{table_name}_log/charge.parquet' (
    FORMAT PARQUET,
    OVERWRITE_OR_IGNORE 1
);