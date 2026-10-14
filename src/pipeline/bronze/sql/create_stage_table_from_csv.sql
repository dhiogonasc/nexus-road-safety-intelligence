CREATE
OR REPLACE TABLE "{schema}"."{table}" AS
SELECT
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
    )