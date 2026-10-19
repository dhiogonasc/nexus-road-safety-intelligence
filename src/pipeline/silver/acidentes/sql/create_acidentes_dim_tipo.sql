CREATE OR REPLACE TABLE "silver"."dim_tipo" AS 
WITH base AS (
    SELECT DISTINCT 
        LOWER(
            REGEXP_REPLACE(
                strip_accents(
                    TRIM(
                        COALESCE(tipo_acidente :: VARCHAR, 'nao_informado')
                    )
                ),
                '[^a-zA-Z0-9]+',
                '_',
                'g'
            )
        ) AS tipo
    FROM "bronze"."ocorrencias"
)
SELECT 
    ROW_NUMBER() OVER (ORDER BY tipo) AS id,
    tipo
FROM base;