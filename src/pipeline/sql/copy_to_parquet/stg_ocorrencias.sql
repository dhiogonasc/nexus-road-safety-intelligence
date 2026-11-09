COPY "silver"."stg_ocorrencias"
TO '{storage_path}/' (
    FORMAT PARQUET,
    PARTITION_BY (ano, uf),
    OVERWRITE_OR_IGNORE 1
);