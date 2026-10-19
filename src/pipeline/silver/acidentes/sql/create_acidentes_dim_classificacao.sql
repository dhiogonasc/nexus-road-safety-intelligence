CREATE OR REPLACE TABLE "silver"."dim_classificacao" AS 
WITH base AS (
    SELECT DISTINCT 
        LOWER(
            REGEXP_REPLACE(
                strip_accents(
                    TRIM(
                        COALESCE(classificacao_acidente :: VARCHAR, 'nao_informado')
                    )
                ),
                '[^a-zA-Z0-9]+',
                '_',
                'g'
            )
        ) AS classificacao
    FROM "bronze"."ocorrencias"
)
SELECT 
    ROW_NUMBER() OVER (ORDER BY classificacao) AS id,
    classificacao
FROM base;