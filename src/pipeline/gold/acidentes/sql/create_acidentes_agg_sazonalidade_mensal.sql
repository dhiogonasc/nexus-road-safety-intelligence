CREATE
OR REPLACE TABLE "gold"."agg_sazonalidade_mensal" AS
SELECT
    md5(
        concat_ws(
            '_',
            COALESCE(t.ano :: VARCHAR, ''),
            COALESCE(t.mes :: VARCHAR, ''),
            COALESCE(l.uf :: VARCHAR, ''),
            COALESCE(c.classificacao_acidente :: VARCHAR, '')
        )
    ) AS id,
    t.ano,
    t.mes,
    l.uf,
    c.classificacao_acidente,
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
    JOIN "silver"."dim_localizacao" AS l ON f.sk_localizacao = l.id
    JOIN "silver"."dim_classificacao" AS c ON f.sk_classificacao = c.id
GROUP BY
    t.ano,
    t.mes,
    l.uf,
    c.classificacao_acidente;