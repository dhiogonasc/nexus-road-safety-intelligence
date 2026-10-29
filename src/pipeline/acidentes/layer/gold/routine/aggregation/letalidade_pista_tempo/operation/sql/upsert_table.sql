CREATE TEMP TABLE temp_dim_local AS SELECT *
FROM read_parquet('{dim_local_storage_path}/**/*.parquet');

CREATE TEMP TABLE temp_dim_pista AS SELECT *
FROM read_parquet('{dim_pista_storage_path}/**/*.parquet');

CREATE TEMP TABLE temp_dim_tempo AS SELECT *
FROM read_parquet('{dim_tempo_storage_path}/**/*.parquet');

CREATE TEMP TABLE temp_dim_clima AS SELECT *
FROM read_parquet('{dim_clima_storage_path}/**/*.parquet');

SELECT setval(
    'seq_letalidade_pista_tempo', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "gold"."agg_letalidade_pista_tempo"), 0), 1)
);

CREATE TEMP TABLE temp_agg_letalidade_pista_tempo AS
SELECT *
FROM (
    SELECT
        local.uf,
        local.br,
        local.area,
        pista.tracado AS tracado_via,
        pista.tipo AS tipo_via,
        tempo.mes,
        tempo.dia_semana,
        tempo.fase_dia,
        clima.classificacao AS classificacao_acidente,
        CAST(COUNT(fato.id) AS BIGINT) AS total_ocorrencias,
        ROUND(CAST(SUM(fato.mortos) AS DOUBLE) / NULLIF(COUNT(fato.id), 0) * 100, 2) AS pct_mortalidade
    FROM
        "gold"."stg" AS fato
        JOIN temp_dim_local AS local ON fato.sk_local = local.id
        JOIN temp_dim_pista AS pista ON fato.sk_pista = pista.id
        JOIN temp_dim_tempo AS tempo ON fato.sk_tempo = tempo.id
        JOIN temp_dim_clima AS clima ON fato.sk_clima = clima.id
    GROUP BY
        local.uf,
        local.br,
        local.area,
        pista.tracado,
        pista.tipo,
        tempo.mes,
        tempo.dia_semana,
        tempo.fase_dia,
        clima.classificacao
);

MERGE INTO "gold"."agg_letalidade_pista_tempo" AS target 
USING temp_agg_letalidade_pista_tempo AS source 
    ON target.uf = source.uf
    AND target.br = source.br
    AND target.area = source.area
    AND target.tracado_via = source.tracado_via
    AND target.tipo_via = source.tipo_via
    AND target.mes = source.mes
    AND target.dia_semana = source.dia_semana
    AND target.fase_dia = source.fase_dia
    AND target.condicao_metereologica = source.condicao_metereologica

WHEN MATCHED THEN
UPDATE SET
    total_ocorrencias = source.total_ocorrencias,
    pct_mortalidade = source.pct_mortalidade

WHEN NOT MATCHED THEN 
INSERT (
    id,
    uf, 
    br,
    area,
    tracado_via,
    tipo_via,
    mes,
    dia_semana,
    fase_dia,
    classificacao_acidente,
    total_ocorrencias,
    pct_mortalidade
) 
VALUES (
    nextval('seq_letalidade_pista_tempo'), 
    source.uf, 
    source.br,
    source.area,
    source.tracado_via,
    source.tipo_via,
    source.mes,
    source.dia_semana,
    source.fase_dia,
    source.classificacao_acidente,
    source.total_ocorrencias,
    source.pct_mortalidade
);

DROP TABLE IF EXISTS temp_dim_local;
DROP TABLE IF EXISTS temp_dim_pista;
DROP TABLE IF EXISTS temp_dim_tempo;
DROP TABLE IF EXISTS temp_dim_clima;
DROP TABLE IF EXISTS temp_agg_letalidade_pista_tempo;