CREATE
OR REPLACE TABLE "bronze"."{table}" AS
SELECT
    md5(concat_ws('|', COLUMNS(* EXCLUDE (filename)))) AS id_carga,
    regexp_extract(filename, '[^/]+$', 0) AS arquivo_fonte,
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
    );

CREATE
OR REPLACE SECRET "{settings.STORAGE_BUCKET}_{table}" (
    TYPE S3,
    PROVIDER CONFIG,
    KEY_ID '{settings.STORAGE_ACCESS_KEY_ID}',
    SECRET '{settings.STORAGE_SECRET_ACCESS_KEY}',
    REGION '{settings.STORAGE_REGION}',
    ENDPOINT '{settings.STORAGE_ENDPOINT}',
    URL_STYLE 'path'
);

COPY "bronze"."{table}" TO 's3://{settings.STORAGE_BUCKET}/{domain}/bronze/{table}/' (
    FORMAT PARQUET,
    PARTITION_BY (arquivo_fonte, data_carga),
    OVERWRITE_OR_IGNORE 1
)