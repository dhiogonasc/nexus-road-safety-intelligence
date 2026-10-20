COPY "bronze"."{table}" TO 's3://{bucket_name}/bronze/{domain}/{table}/' (
    FORMAT PARQUET,
    PARTITION_BY (arquivo_fonte, data_carga),
    OVERWRITE_OR_IGNORE 1
);