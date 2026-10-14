CREATE
OR REPLACE TABLE "acidentes"."dim_pista" AS WITH base_pista AS (
    SELECT
        DISTINCT LOWER(
            REGEXP_REPLACE(
                strip_accents(
                    TRIM(
                        COALESCE(condicao_metereologica :: VARCHAR, 'nao_informado')
                    )
                ),
                '[^a-zA-Z0-9]+',
                '_',
                'g'
            )
        ) AS condicao_metereologica,
        LOWER(
            REGEXP_REPLACE(
                strip_accents(
                    TRIM(
                        COALESCE(sentido_via :: VARCHAR, 'nao_informado')
                    )
                ),
                '[^a-zA-Z0-9]+',
                '_',
                'g'
            )
        ) AS sentido_via,
        LOWER(
            REGEXP_REPLACE(
                strip_accents(
                    TRIM(
                        COALESCE(tracado_via :: VARCHAR, 'nao_informado')
                    )
                ),
                '[^a-zA-Z0-9]+',
                '_',
                'g'
            )
        ) AS tracado_via,
        LOWER(
            REGEXP_REPLACE(
                strip_accents(
                    TRIM(
                        COALESCE(tipo_pista :: VARCHAR, 'nao_informado')
                    )
                ),
                '[^a-zA-Z0-9]+',
                '_',
                'g'
            )
        ) AS tipo_pista,
        LOWER(
            REGEXP_REPLACE(
                strip_accents(
                    TRIM(
                        COALESCE(uso_solo :: VARCHAR, 'nao_informado')
                    )
                ),
                '[^a-zA-Z0-9]+',
                '_',
                'g'
            )
        ) AS uso_solo
    FROM
        "acidentes"."stg_ocorrencias"
),
ref_pista AS (
    SELECT
        *,
        md5(
            concat_ws(
                '_',
                COALESCE(condicao_metereologica, ''),
                COALESCE(sentido_via, ''),
                COALESCE(tracado_via, ''),
                COALESCE(tipo_pista, ''),
                COALESCE(uso_solo, '')
            )
        ) AS id
    FROM
        base_pista
)
SELECT
    id,
    sentido_via,
    condicao_metereologica,
    tipo_pista,
    tracado_via,
    uso_solo
FROM
    ref_pista;