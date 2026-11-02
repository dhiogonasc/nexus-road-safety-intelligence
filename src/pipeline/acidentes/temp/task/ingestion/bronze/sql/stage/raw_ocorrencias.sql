CREATE OR REPLACE TABLE "bronze"."raw_ocorrencias" AS
SELECT
    strftime(CURRENT_TIMESTAMP, '%Y-%m-%d_%H-%M-%S') AS data_carga,
    *
FROM
    read_csv_auto(
        '{csv_path}',
        delim = '{delim}',
        encoding = '{encoding}',
        header = TRUE,
        auto_detect = TRUE,
        normalize_names = TRUE,
        union_by_name = TRUE
    );