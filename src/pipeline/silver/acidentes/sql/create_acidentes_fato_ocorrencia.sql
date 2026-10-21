CREATE OR REPLACE TABLE "silver"."fato_ocorrencia" AS 
WITH origin AS (
    SELECT
        id AS id_ocorrencia,
        TRIM(COALESCE(uf :: VARCHAR, 'nao_informado'))AS uf,
        TRIM(COALESCE(br :: VARCHAR, 'nao_informado')) AS br,
        TRIM(COALESCE(municipio :: VARCHAR, 'nao_informado')) AS municipio,
        TRIM(COALESCE(regional :: VARCHAR, 'nao_informado')) AS regional,
        TRIM(COALESCE(delegacia :: VARCHAR, 'nao_informado')) AS delegacia,
        TRIM(COALESCE(uop :: VARCHAR, 'nao_informado')) AS uop,
        TRY_CAST(REPLACE(km :: VARCHAR, ',', '.') AS DOUBLE) AS km,
        TRY_CAST(REPLACE(latitude :: VARCHAR, ',', '.') AS DOUBLE) AS latitude,
        TRY_CAST(REPLACE(longitude :: VARCHAR, ',', '.') AS DOUBLE) AS longitude,
        COALESCE(causa_acidente :: VARCHAR, 'nao_informado') AS causa_acidente,
        COALESCE(tipo_acidente :: VARCHAR, 'nao_informado') AS tipo_acidente,
        COALESCE(classificacao_acidente :: VARCHAR, 'nao_informado') AS classificacao_acidente,
        COALESCE(condicao_metereologica :: VARCHAR, 'nao_informado') AS condicao_metereologica,
        COALESCE(sentido_via :: VARCHAR, 'nao_informado') AS sentido_via,
        COALESCE(tracado_via :: VARCHAR, 'nao_informado') AS tracado_via,
        COALESCE(tipo_pista :: VARCHAR, 'nao_informado') AS tipo_pista,
        COALESCE(uso_solo :: VARCHAR, 'nao_informado') AS uso_solo,
        pessoas,
        mortos,
        feridos_leves,
        feridos_graves,
        feridos,
        ilesos,
        ignorados,
        veiculos
    FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet')
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
            COALESCE(p.id :: VARCHAR, ''),
            COALESCE(cond.id :: VARCHAR, '')
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
    cond.id AS sk_condicao_metereologica,
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
    LEFT JOIN "silver".dim_tempo AS t 
        ON o.data_hora = t.data_hora
    LEFT JOIN "silver".dim_localizacao AS l 
        ON o.uf = l.uf 
       AND o.br = l.br 
       AND o.km = l.km
       AND o.municipio = l.municipio 
       AND o.regional = l.regional 
       AND o.delegacia = l.delegacia 
       AND o.uop = l.uop
    LEFT JOIN "silver".dim_coordenada AS coord 
        ON o.latitude = coord.latitude 
       AND o.longitude = coord.longitude
    LEFT JOIN "silver".dim_causa AS causa 
        ON o.causa_acidente = causa.causa
    LEFT JOIN "silver".dim_tipo AS tipo 
        ON o.tipo_acidente = tipo.tipo
    LEFT JOIN "silver".dim_classificacao AS classif 
        ON o.classificacao_acidente = classif.classificacao
    LEFT JOIN "silver".dim_pista AS p 
        ON o.sentido_via = p.sentido
       AND o.tracado_via = p.tracado
       AND o.tipo_pista = p.tipo
       AND o.uso_solo = p.uso_solo
    LEFT JOIN "silver".dim_condicao_metereologica AS cond
        ON o.condicao_metereologica = cond.condicao;