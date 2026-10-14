CREATE
OR REPLACE TABLE "acidentes"."fato_ocorrencia" AS WITH origin AS (
    SELECT
        id AS id_ocorrencia,
        (
            TRY_CAST(data_inversa AS DATE) + TRY_CAST(horario AS TIME)
        ) AS data_hora,
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
        ) AS uop,
        TRY_CAST(REPLACE(km :: VARCHAR, ',', '.') AS DOUBLE) AS km,
        TRY_CAST(REPLACE(latitude :: VARCHAR, ',', '.') AS DOUBLE) AS latitude,
        TRY_CAST(REPLACE(longitude :: VARCHAR, ',', '.') AS DOUBLE) AS longitude,
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
                        COALESCE(classificacao_acidente :: VARCHAR, 'nao_informado')
                    )
                ),
                '[^a-zA-Z0-9]+',
                '_',
                'g'
            )
        ) AS classificacao_acidente,
        LOWER(
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
        ) AS uso_solo,
        pessoas,
        mortos,
        feridos_leves,
        feridos_graves,
        feridos,
        ilesos,
        ignorados,
        veiculos
    FROM
        "acidentes"."stg_ocorrencias"
)
SELECT
    md5(
        concat_ws(
            '_',
            COALESCE(o.id_ocorrencia :: VARCHAR, ''),
            COALESCE(t.id :: VARCHAR, ''),
            COALESCE(l.id :: VARCHAR, ''),
            COALESCE(c.id :: VARCHAR, ''),
            COALESCE(p.id :: VARCHAR, '')
        )
    ) AS id,
    o.id_ocorrencia,
    t.id AS sk_tempo,
    l.id AS sk_localizacao,
    c.id AS sk_classificacao,
    p.id AS sk_pista,
    o.pessoas,
    o.mortos,
    o.feridos_leves,
    o.feridos_graves,
    o.feridos,
    o.ilesos,
    o.ignorados,
    o.veiculos
FROM
    origin AS o
    LEFT JOIN "acidentes".dim_tempo AS t ON o.data_hora = t.data_hora
    LEFT JOIN "acidentes".dim_localizacao AS l ON l.uf = o.uf
    AND l.br = o.br
    AND l.municipio = o.municipio
    AND l.regional = o.regional
    AND l.delegacia = o.delegacia
    AND l.uop = o.uop
    AND l.km IS NOT DISTINCT
FROM
    o.km
    AND l.latitude IS NOT DISTINCT
FROM
    o.latitude
    AND l.longitude IS NOT DISTINCT
FROM
    o.longitude
    LEFT JOIN "acidentes".dim_classificacao AS c ON c.causa_acidente = o.causa_acidente
    AND c.tipo_acidente = o.tipo_acidente
    AND c.classificacao_acidente = o.classificacao_acidente
    LEFT JOIN "acidentes".dim_pista AS p ON p.sentido_via = o.sentido_via
    AND p.condicao_metereologica = o.condicao_metereologica
    AND p.tipo_pista = o.tipo_pista
    AND p.tracado_via = o.tracado_via
    AND p.uso_solo = o.uso_solo;