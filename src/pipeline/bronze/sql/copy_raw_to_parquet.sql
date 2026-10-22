COPY (
    SELECT
        strftime(CURRENT_TIMESTAMP, '%Y-%m-%d_%H-%M-%S') AS data_carga,
        regexp_extract(filename, '([^/]+)\.[^./]+$', 1) AS arquivo_fonte,
        *
    FROM
        read_csv_auto(
            '{csv_path}',
            filename = TRUE,
            delim = '{delim}',
            encoding = '{encoding}',
            header = TRUE,
            auto_detect = TRUE,
            normalize_names = TRUE,
            union_by_name = TRUE
        )
) TO 's3://{settings.STORAGE_BUCKET}/{domain}/bronze/{table_name}/' (
    FORMAT PARQUET,
    PARTITION_BY (data_carga, arquivo_fonte),
    OVERWRITE_OR_IGNORE 1
);