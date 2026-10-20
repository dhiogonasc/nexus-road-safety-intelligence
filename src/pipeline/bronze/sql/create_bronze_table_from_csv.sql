CREATE
OR REPLACE TABLE "bronze"."{table}" AS
SELECT
    md5(concat_ws('|', COLUMNS(* EXCLUDE (filename)))) AS id_carga,
    filename AS arquivo_fonte,
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