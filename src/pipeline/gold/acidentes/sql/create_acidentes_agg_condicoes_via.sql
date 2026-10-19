CREATE OR REPLACE TABLE "gold"."agg_condicoes_via" AS
SELECT
    md5(
        concat_ws(
            '_',
            COALESCE(t.ano :: VARCHAR, ''),
            COALESCE(t.mes :: VARCHAR, ''),
            COALESCE(t.dia :: VARCHAR, ''),
            COALESCE(t.dia_semana :: VARCHAR, ''),
            COALESCE(t.fase_dia :: VARCHAR, ''),
            COALESCE(p.condicao_metereologica :: VARCHAR, ''),
            COALESCE(p.sentido_via :: VARCHAR, ''),
            COALESCE(p.tracado_via :: VARCHAR, ''),
            COALESCE(p.tipo_pista :: VARCHAR, ''),
            COALESCE(p.uso_solo :: VARCHAR, '')
        )
    ) AS id,
    t.ano,
    t.mes,
    t.dia,
    t.dia_semana,
    t.fase_dia,
    p.condicao_metereologica,
    p.sentido_via,
    p.tracado_via,
    p.tipo_pista,
    p.uso_solo,
    CAST(COUNT(f.id) AS BIGINT) AS total_ocorrencias,
    CAST(SUM(f.pessoas) AS BIGINT) AS total_pessoas,
    CAST(SUM(f.veiculos) AS BIGINT) AS total_veiculos,
    CAST(SUM(f.mortos) AS BIGINT) AS total_mortos,
    CAST(SUM(f.feridos) AS BIGINT) AS total_feridos,
    CAST(SUM(f.feridos_graves) AS BIGINT) AS total_feridos_graves,
    CAST(SUM(f.feridos_leves) AS BIGINT) AS total_feridos_leves,
    CAST(SUM(f.ilesos) AS BIGINT) AS total_ilesos,
    ROUND(
        CAST(SUM(f.mortos) AS DOUBLE) / NULLIF(COUNT(f.id), 0) * 100,
        2
    ) AS pct_mortalidade
FROM
    "silver"."fato_ocorrencia" AS f
    JOIN "silver"."dim_tempo" AS t ON f.sk_tempo = t.id
    JOIN "silver"."dim_pista" AS p ON f.sk_pista = p.id
GROUP BY
    t.ano,
    t.mes,
    t.dia,
    t.dia_semana,
    t.fase_dia,
    p.condicao_metereologica,
    p.sentido_via,
    p.tracado_via,
    p.tipo_pista,
    p.uso_solo;