CREATE TEMP TABLE temp_dim_local AS SELECT *
FROM read_parquet('{dim_local_storage_path}/**/*.parquet');

CREATE TEMP TABLE temp_dim_tempo AS SELECT *
FROM read_parquet('{dim_tempo_storage_path}/**/*.parquet');

SELECT setval(
    'seq_dispersao_geo_temporal', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "gold"."agg_dispersao_geo_temporal"), 0), 1)
);

CREATE TEMP TABLE temp_agg_dispersao_geo_temporal AS
SELECT *
FROM (
    SELECT
        local.uf,
        local.area,
        local.municipio,
        tempo.ano,
        tempo.mes,
        tempo.dia_semana,
        CAST(COUNT(fato.id) AS BIGINT) AS total_ocorrencias,
        ROUND(CAST(SUM(fato.mortos) AS DOUBLE) / NULLIF(COUNT(fato.id), 0) * 100, 2) AS pct_mortalidade
    FROM
        "gold"."stg_ft_ocorrencia" AS fato
        JOIN temp_dim_local AS local ON fato.sk_local = local.id
        JOIN temp_dim_tempo AS tempo ON fato.sk_tempo = tempo.id
    GROUP BY
        local.uf,
        local.area,
        local.municipio,
        tempo.ano,
        tempo.mes,
        tempo.dia_semana
);

MERGE INTO "gold"."agg_dispersao_geo_temporal" AS target 
USING temp_agg_dispersao_geo_temporal AS source 
    ON target.uf = source.uf
    AND target.area = source.area
    AND target.municipio = source.municipio
    AND target.ano = source.ano
    AND target.mes = source.mes
    AND target.dia_semana = source.dia_semana

WHEN MATCHED THEN
UPDATE SET
    total_ocorrencias = source.total_ocorrencias,
    pct_mortalidade = source.pct_mortalidade

WHEN NOT MATCHED THEN 
INSERT (
    id,
    uf, 
    area, 
    municipio,
    ano,
    mes,
    dia_semana,
    total_ocorrencias,
    pct_mortalidade
) 
VALUES (
    nextval('seq_dispersao_geo_temporal'),
    source.uf,
    source.area,
    source.municipio,
    source.ano,
    source.mes,
    source.dia_semana,
    source.total_ocorrencias,
    source.pct_mortalidade
);

DROP TABLE IF EXISTS temp_dim_local;
DROP TABLE IF EXISTS temp_dim_tempo;
DROP TABLE IF EXISTS temp_agg_dispersao_geo_temporal;