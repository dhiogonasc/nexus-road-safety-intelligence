CREATE OR REPLACE TABLE "silver"."dim_localizacao" AS 
WITH base AS (
    SELECT DISTINCT 
        LOWER(
            REGEXP_REPLACE(
                strip_accents(
                    TRIM(COALESCE(uf :: VARCHAR, 'nao_informado'))
                ),
                '[^a-zA-Z0-9]+',
                '_',
                'g'
            )
        ) AS uf,
        LOWER(
            REGEXP_REPLACE(
                strip_accents(
                    TRIM(COALESCE(br :: VARCHAR, 'nao_informado'))
                ),
                '[^a-zA-Z0-9]+',
                '_',
                'g'
            )
        ) AS br,
        LOWER(
            REGEXP_REPLACE(
                strip_accents(
                    TRIM(COALESCE(municipio :: VARCHAR, 'nao_informado'))
                ),
                '[^a-zA-Z0-9]+',
                '_',
                'g'
            )
        ) AS municipio,
        LOWER(
            REGEXP_REPLACE(
                strip_accents(
                    TRIM(COALESCE(regional :: VARCHAR, 'nao_informado'))
                ),
                '[^a-zA-Z0-9]+',
                '_',
                'g'
            )
        ) AS regional,
        LOWER(
            REGEXP_REPLACE(
                strip_accents(
                    TRIM(COALESCE(delegacia :: VARCHAR, 'nao_informado'))
                ),
                '[^a-zA-Z0-9]+',
                '_',
                'g'
            )
        ) AS delegacia,
        LOWER(
            REGEXP_REPLACE(
                strip_accents(
                    TRIM(COALESCE(uop :: VARCHAR, 'nao_informado'))
                ),
                '[^a-zA-Z0-9]+',
                '_',
                'g'
            )
        ) AS uop
    FROM "bronze"."ocorrencias"
)
SELECT 
    ROW_NUMBER() OVER (ORDER BY uf, br, municipio, regional, delegacia, uop) AS id,
    uf,
    br,
    municipio,
    regional,
    delegacia,
    uop
FROM base;