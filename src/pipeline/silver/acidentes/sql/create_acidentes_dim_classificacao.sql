CREATE
OR REPLACE TABLE "silver"."dim_classificacao" AS WITH base_acidente AS (
    SELECT
        DISTINCT LOWER(
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
        ) AS causa_acidente,
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
        ) AS tipo_acidente,
        LOWER(
            REGEXP_REPLACE(
                strip_accents(
                    TRIM(
                        COALESCE(
                            classificacao_acidente :: VARCHAR,
                            'nao_informado'
                        )
                    )
                ),
                '[^a-zA-Z0-9]+',
                '_',
                'g'
            )
        ) AS classificacao_acidente
    FROM
        "bronze"."ocorrencias"
),
ref_acidente AS (
    SELECT
        *,
        md5(
            concat_ws(
                '_',
                COALESCE(causa_acidente, ''),
                COALESCE(tipo_acidente, ''),
                COALESCE(classificacao_acidente, '')
            )
        ) AS id
    FROM
        base_acidente
)
SELECT
    id,
    causa_acidente,
    tipo_acidente,
    classificacao_acidente
FROM
    ref_acidente;