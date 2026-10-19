CREATE OR REPLACE TABLE "silver"."fato_ocorrencia" AS 
WITH origin AS (
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
        TRY_CAST(
            REPLACE(longitude :: VARCHAR, ',', '.') AS DOUBLE
        ) AS longitude,
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
        ) AS classificacao_acidente,
        LOWER(
            REGEXP_REPLACE(
                strip_accents(
                    TRIM(
                        COALESCE(
                            condicao_metereologica :: VARCHAR,
                            'nao_informado'
                        )
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
        "bronze"."ocorrencias"
),
origin_with_keys AS (
    SELECT
        o.*,
        md5(
            concat_ws(
                '_',
                COALESCE(o.condicao_metereologica, ''),
                COALESCE(o.sentido_via, ''),
                COALESCE(o.tracado_via, ''),
                COALESCE(o.tipo_pista, ''),
                COALESCE(o.uso_solo, '')
            )
        ) AS calculated_sk_pista
    FROM
        origin AS o
)
SELECT
    md5(
        concat_ws(
            '_',
            COALESCE(o.id_ocorrencia :: VARCHAR, ''),
            COALESCE(t.id :: VARCHAR, ''),
            COALESCE(l.id :: VARCHAR, ''),
            COALESCE(coord.id :: VARCHAR, ''),
            COALESCE(causa.id :: VARCHAR, ''),
            COALESCE(tipo.id :: VARCHAR, ''),
            COALESCE(classif.id :: VARCHAR, ''),
            COALESCE(p.id :: VARCHAR, '')
        )
    ) AS id,
    o.id_ocorrencia,
    t.id AS sk_tempo,
    l.id AS sk_localizacao,
    coord.id AS sk_coordenada,
    causa.id AS sk_causa,
    tipo.id AS sk_tipo,
    classif.id AS sk_classificacao,
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
    origin_with_keys AS o
    LEFT JOIN "silver".dim_tempo AS t 
        ON o.data_hora = t.data_hora
    LEFT JOIN "silver".dim_localizacao AS l 
        ON o.uf = l.uf 
       AND o.br = l.br 
       AND o.municipio = l.municipio 
       AND o.regional = l.regional 
       AND o.delegacia = l.delegacia 
       AND o.uop = l.uop
    LEFT JOIN "silver".dim_coordenada AS coord 
        ON o.km = coord.km 
       AND o.latitude = coord.latitude 
       AND o.longitude = coord.longitude
    LEFT JOIN "silver".dim_causa AS causa 
        ON o.causa_acidente = causa.causa
    LEFT JOIN "silver".dim_tipo AS tipo 
        ON o.tipo_acidente = tipo.tipo
    LEFT JOIN "silver".dim_classificacao AS classif 
        ON o.classificacao_acidente = classif.classificacao
    LEFT JOIN "silver".dim_pista AS p 
        ON o.calculated_sk_pista = p.id;