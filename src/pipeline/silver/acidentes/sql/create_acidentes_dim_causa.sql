CREATE OR REPLACE TABLE "silver"."dim_causa" AS 
WITH base AS (
    SELECT DISTINCT 
        LOWER(
            REGEXP_REPLACE(
                strip_accents(
                    TRIM(
                        COALESCE(causa_acidente :: VARCHAR, 'nao_informado')
                    )
                ),
                '[^a-zA-Z0-9]+',
                '_',
                'g'
            )
        ) AS causa
    FROM "bronze"."ocorrencias"
)
SELECT 
    ROW_NUMBER() OVER (ORDER BY causa) AS id,
    causa
FROM base;