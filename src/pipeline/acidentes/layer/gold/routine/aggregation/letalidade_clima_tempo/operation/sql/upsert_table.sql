CREATE TEMP TABLE temp_dim_local AS SELECT *
FROM read_parquet('{dim_local_storage_path}/**/*.parquet');

CREATE TEMP TABLE temp_dim_clima AS SELECT *
FROM read_parquet('{dim_clima_storage_path}/**/*.parquet');

CREATE TEMP TABLE temp_dim_tempo AS SELECT *
FROM read_parquet('{dim_tempo_storage_path}/**/*.parquet');

CREATE TEMP TABLE temp_dim_categoria AS SELECT *
FROM read_parquet('{dim_categoria_storage_path}/**/*.parquet');

SELECT setval(
    'seq_letalidade_clima_tempo', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "gold"."agg_letalidade_clima_tempo"), 0), 1)
);

CREATE TEMP TABLE temp_agg_letalidade_clima_tempo AS
SELECT *
FROM (
    SELECT
        local.uf,
        local.area,
        clima.condicao AS condicao_metereologica,
        tempo.mes,
        tempo.fase_dia,
        categoria.classificacao AS classificacao_acidente,
        CAST(COUNT(fato.id) AS BIGINT) AS total_ocorrencias,
        ROUND(CAST(SUM(fato.mortos) AS DOUBLE) / NULLIF(COUNT(fato.id), 0) * 100, 2) AS pct_mortalidade
    FROM
        "gold"."stg" AS fato
        JOIN temp_dim_local AS local ON fato.sk_local = local.id
        JOIN temp_dim_clima AS clima ON fato.sk_clima = clima.id
        JOIN temp_dim_tempo AS tempo ON fato.sk_tempo = tempo.id
        JOIN temp_dim_categoria AS causa ON fato.sk_causa = causa.id
    GROUP BY
        local.uf,
        local.area,
        clima.condicao,
        tempo.mes,
        tempo.fase_dia,
        categoria.classificacao
);

MERGE INTO "gold"."agg_letalidade_clima_tempo" AS target 
USING temp_agg_letalidade_clima_tempo AS source 
    ON target.uf = source.uf
    AND target.area = source.area
    AND target.condicao = source.condicao
    AND target.mes = source.mes
    AND target.fase_dia = source.fase_dia
    AND target.classificacao = source.classificacao

WHEN MATCHED THEN
UPDATE SET
    total_ocorrencias = source.total_ocorrencias,
    pct_mortalidade = source.pct_mortalidade

WHEN NOT MATCHED THEN 
INSERT (
    id,
    uf, 
    area,
    condicao_metereologica,
    mes,
    fase_dia,
    classificacao_acidente,
    total_ocorrencias,
    pct_mortalidade
) 
VALUES (
    nextval('seq_letalidade_clima_tempo') AS id,
    source.uf, 
    source.area,
    source.condicao_metereologica,
    source.mes,
    source.fase_dia,
    source.classificacao_acidente,
    source.total_ocorrencias,
    source.pct_mortalidade
);

DROP TABLE IF EXISTS temp_dim_local;
DROP TABLE IF EXISTS temp_dim_pista;
DROP TABLE IF EXISTS temp_dim_clima;
DROP TABLE IF EXISTS temp_dim_categoria;
DROP TABLE IF EXISTS temp_agg_letalidade_clima_tempo;