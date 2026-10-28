CREATE TEMP TABLE temp_dim_localizacao AS SELECT *
FROM read_parquet('{dim_localizacao_storage_path}/**/*.parquet');

CREATE TEMP TABLE temp_dim_tempo AS SELECT *
FROM read_parquet('{dim_tempo_storage_path}/**/*.parquet');

SELECT setval(
    'seq_dispersao_geo_temporal', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "gold"."agg_dispersao_geo_temporal"), 0), 1)
);

CREATE TEMP TABLE temp_agg_dispersao_geo_temporal AS
SELECT nextval('seq_dispersao_geo_temporal') AS id, *
FROM (
    SELECT
        localizacao.uf,
        localizacao.br,
        localizacao.municipio,

        tempo.ano,
        tempo.mes,
        tempo.dia_semana,

        CAST(COUNT(fato.id) AS BIGINT) AS total_ocorrencias,
        CAST(SUM(fato.pessoas) AS BIGINT) AS total_pessoas,
        CAST(SUM(fato.veiculos) AS BIGINT) AS total_veiculos,
        CAST(SUM(fato.mortos) AS BIGINT) AS total_mortos,
        CAST(SUM(fato.feridos) AS BIGINT) AS total_feridos,
        CAST(SUM(fato.feridos_graves) AS BIGINT) AS total_feridos_graves,
        CAST(SUM(fato.feridos_leves) AS BIGINT) AS total_feridos_leves,
        CAST(SUM(fato.ilesos) AS BIGINT) AS total_ilesos,
        ROUND(CAST(SUM(fato.mortos) AS DOUBLE) / NULLIF(COUNT(fato.id), 0) * 100, 2) AS pct_mortalidade
    FROM
        "gold"."stg" AS fato
        JOIN temp_dim_localizacao AS localizacao ON fato.sk_localizacao = localizacao.id
        JOIN temp_dim_tempo AS tempo ON fato.sk_tempo = tempo.id
    GROUP BY
        localizacao.uf,
        localizacao.br,
        localizacao.municipio,

        tempo.ano,
        tempo.mes,
        tempo.dia_semana
);

MERGE INTO "gold"."agg_dispersao_geo_temporal" AS target 
USING temp_agg_dispersao_geo_temporal AS source 
    ON target.id = source.id

WHEN MATCHED THEN
UPDATE SET
    total_ocorrencias = source.total_ocorrencias,
    total_pessoas = source.total_pessoas,
    total_veiculos = source.total_veiculos,
    total_mortos = source.total_mortos,
    total_feridos = source.total_feridos,
    total_feridos_graves = source.total_feridos_graves,
    total_feridos_leves = source.total_feridos_leves,
    total_ilesos = source.total_ilesos,
    pct_mortalidade = source.pct_mortalidade

WHEN NOT MATCHED THEN 
INSERT (
    id,

    uf, 
    br, 
    municipio,

    ano,
    mes,
    dia_semana,

    total_ocorrencias,
    total_pessoas,
    total_veiculos,
    total_mortos,
    total_feridos,
    total_feridos_graves,
    total_feridos_leves,
    total_ilesos,
    pct_mortalidade
) 
VALUES (
    source.id,

    source.uf,
    source.br,
    source.municipio,

    source.ano,
    source.mes,
    source.dia_semana,

    source.total_ocorrencias,
    source.total_pessoas,
    source.total_veiculos,
    source.total_mortos,
    source.total_feridos,
    source.total_feridos_graves,
    source.total_feridos_leves,
    source.total_ilesos,
    source.pct_mortalidade
);

DROP TABLE IF EXISTS temp_dim_localizacao;
DROP TABLE IF EXISTS temp_dim_tempo;

DROP TABLE IF EXISTS temp_agg_dispersao_geo_temporal;