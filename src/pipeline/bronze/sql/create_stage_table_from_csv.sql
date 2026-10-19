CREATE OR REPLACE TABLE "bronze"."{table}" AS 
SELECT 
    *,
    filename AS arquivo_fonte,
    CURRENT_TIMESTAMP AS data_carga,
FROM read_csv_auto(
    '{csv_path}',
    delim = '{delim}',
    encoding = '{encoding}',
    header = TRUE,
    auto_detect = TRUE,
    normalize_names = TRUE,
    union_by_name = TRUE,
    filename = TRUE
);