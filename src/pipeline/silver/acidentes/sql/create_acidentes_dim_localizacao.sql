CREATE
OR REPLACE TABLE "silver"."dim_localizacao" AS WITH base_localizacao AS (
    SELECT
        DISTINCT LOWER(
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
        ) AS uop,
        TRY_CAST(REPLACE(km :: VARCHAR, ',', '.') AS DOUBLE) AS km,
        TRY_CAST(REPLACE(latitude :: VARCHAR, ',', '.') AS DOUBLE) AS latitude,
        TRY_CAST(
            REPLACE(longitude :: VARCHAR, ',', '.') AS DOUBLE
        ) AS longitude
    FROM
        "bronze"."ocorrencias"
),
ref_localizacao AS (
    SELECT
        *,
        md5(
            concat_ws(
                '_',
                COALESCE(uf, ''),
                COALESCE(br, ''),
                COALESCE(km :: VARCHAR, ''),
                COALESCE(municipio, ''),
                COALESCE(regional, ''),
                COALESCE(delegacia, ''),
                COALESCE(uop, ''),
                COALESCE(latitude :: VARCHAR, ''),
                COALESCE(longitude :: VARCHAR, '')
            )
        ) AS id
    FROM
        base_localizacao
)
SELECT
    id,
    uf,
    br,
    km,
    municipio,
    regional,
    delegacia,
    uop,
    latitude,
    longitude
FROM
    ref_localizacao;