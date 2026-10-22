CREATE TEMP TABLE temp_fato_ocorrencia AS SELECT *
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/fato_ocorrencia/fato_ocorrencia.parquet') ;

CREATE TEMP TABLE temp_dim_tempo AS SELECT *
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/dim_tempo/dim_tempo.parquet');

CREATE TEMP TABLE temp_dim_localizacao AS SELECT *
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/dim_localizacao/dim_localizacao.parquet');
    
CREATE TEMP TABLE temp_agg_trechos_criticos AS
SELECT COALESCE((SELECT MAX(id) FROM "gold"."agg_trechos_criticos"), 0) + ROW_NUMBER() OVER () AS id, source_data.*
FROM (
    SELECT
        tempo.ano,
        tempo.mes,
        tempo.dia,
        tempo.dia_semana,
        tempo.fase_dia,
        localizacao.uf,
        localizacao.br,
        localizacao.km,
        localizacao.municipio,
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
        JOIN temp_dim_localizacao AS localizacao ON fato.sk_localizacao = localizacao.id
    GROUP BY
        tempo.ano,
        tempo.mes,
        tempo.dia,
        tempo.dia_semana,
        tempo.fase_dia,
        localizacao.uf,
        localizacao.br,
        localizacao.km,
        localizacao.municipio

) AS source_data;

MERGE INTO "gold"."agg_trechos_criticos" AS target 
USING temp_agg_trechos_criticos AS source 
    ON target.ano = source.ano 
    AND target.mes = source.mes 
    AND target.dia = source.dia 
    AND target.dia_semana = source.dia_semana 
    AND target.fase_dia = source.fase_dia
    AND target.uf = source.uf 
    AND target.br = source.br 
    AND target.km = source.km
    AND target.municipio = source.municipio 

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
    uf,
    br,
    km,
    municipio,
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
    source.uf,
    source.br,
    source.km,
    source.municipio,
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
DROP TABLE IF EXISTS temp_dim_localizacao;
DROP TABLE IF EXISTS temp_agg_trechos_criticos;