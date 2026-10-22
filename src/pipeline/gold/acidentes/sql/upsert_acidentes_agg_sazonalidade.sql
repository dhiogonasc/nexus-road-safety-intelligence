CREATE TEMP TABLE temp_fato_ocorrencia 
AS SELECT *
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/fato_ocorrencia/fato_ocorrencia.parquet') ;

CREATE TEMP TABLE temp_dim_tempo 
AS SELECT *
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/dim_tempo/dim_tempo.parquet');

CREATE TEMP TABLE temp_dim_causa 
AS SELECT *
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/dim_causa/dim_causa.parquet');

CREATE TEMP TABLE temp_dim_tipo 
AS SELECT *
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/dim_tipo/dim_tipo.parquet');

CREATE TEMP TABLE temp_dim_classificacao 
AS SELECT *
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/dim_classificacao/dim_classificacao.parquet');
    
CREATE TEMP TABLE temp_agg_sazonalidade AS
SELECT COALESCE((SELECT MAX(id) FROM "gold"."agg_sazonalidade"), 0) + ROW_NUMBER() OVER () AS id, source_data.*
FROM (
    SELECT
        tempo.ano,
        tempo.mes,
        tempo.dia,
        tempo.dia_semana,
        tempo.fase_dia,
        causa.causa as causa_acidente,
        tipo.tipo as tipo_acidente,
        classificacao.classificacao classificacao_acidente,
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
        temp_fato_ocorrencia AS fato
        JOIN temp_dim_tempo AS tempo ON fato.sk_tempo = tempo.id
        JOIN temp_dim_causa AS causa ON fato.sk_causa = causa.id
        JOIN temp_dim_tipo AS tipo ON fato.sk_tipo = tipo.id
        JOIN temp_dim_classificacao AS classificacao ON fato.sk_classificacao = classificacao.id
    GROUP BY
        tempo.ano,
        tempo.mes,
        tempo.dia,
        tempo.dia_semana,
        tempo.fase_dia,
        causa.causa,
        tipo.tipo,
        classificacao.classificacao
) AS source_data;

MERGE INTO "gold"."agg_sazonalidade" AS target 
USING temp_agg_sazonalidade AS source 
    ON target.ano = source.ano
    AND target.mes = source.mes
    AND target.dia = source.dia
    AND target.dia_semana = source.dia_semana
    AND target.fase_dia = source.fase_dia
    AND target.causa_acidente = source.causa_acidente
    AND target.tipo_acidente = source.tipo_acidente
    AND target.classificacao_acidente = source.classificacao_acidente

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
    ano,
    mes,
    dia,
    dia_semana,
    fase_dia,
    causa_acidente,
    tipo_acidente,
    classificacao_acidente,
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
    source.ano,
    source.mes,
    source.dia,
    source.dia_semana,
    source.fase_dia,
    source.causa_acidente,
    source.tipo_acidente,
    source.classificacao_acidente,
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

DROP TABLE IF EXISTS temp_fato_ocorrencia;
DROP TABLE IF EXISTS temp_dim_tempo;
DROP TABLE IF EXISTS temp_dim_causa;
DROP TABLE IF EXISTS temp_dim_tipo;
DROP TABLE IF EXISTS temp_dim_classificacao;
DROP TABLE IF EXISTS temp_agg_sazonalidade;