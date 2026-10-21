COPY (
    SELECT
        md5(concat_ws('|', COLUMNS(* EXCLUDE (filename)))) AS id_carga,
        regexp_extract(filename, '([^/]+)\.[^./]+$', 1) AS arquivo_fonte,
        CAST(CURRENT_TIMESTAMP AS DATE) AS data_carga,
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
    PARTITION_BY (arquivo_fonte, data_carga),
    OVERWRITE_OR_IGNORE 1
);