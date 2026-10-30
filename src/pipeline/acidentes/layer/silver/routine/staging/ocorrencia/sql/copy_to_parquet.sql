COPY "silver"."stg_ocorrencia" 
TO '{storage_path}/' (
    FORMAT PARQUET,
    PARTITION_BY (ano, uf),
    OVERWRITE_OR_IGNORE 1
);