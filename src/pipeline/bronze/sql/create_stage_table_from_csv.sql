CREATE TABLE IF NOT EXISTS "bronze"."{table}" AS 
SELECT 
    *,
    CAST('' AS VARCHAR) AS arquivo_fonte,
    CURRENT_TIMESTAMP AS data_carga,
    CAST('' AS VARCHAR) AS stage_id
FROM read_csv_auto(
    '{csv_path}',
    delim = '{delim}',
    encoding = '{encoding}',
    header = TRUE,
    auto_detect = TRUE,
    normalize_names = TRUE,
    union_by_name = TRUE,
    filename = TRUE
)
WHERE 1 = 0;

CREATE TEMP TABLE "temp_{table}" AS 
SELECT 
    *, 
    filename AS arquivo_fonte 
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

INSERT INTO "bronze"."{table}"
SELECT 
    t.*,
    CURRENT_TIMESTAMP AS data_carga,
    md5(concat_ws('|', CAST(t AS VARCHAR), CAST(CURRENT_TIMESTAMP AS VARCHAR))) AS stage_id
FROM "temp_{table}" AS t
QUALIFY ROW_NUMBER() OVER (PARTITION BY COLUMNS(* EXCLUDE (arquivo_fonte))) = 1;

DROP TABLE IF EXISTS "temp_{table}";
