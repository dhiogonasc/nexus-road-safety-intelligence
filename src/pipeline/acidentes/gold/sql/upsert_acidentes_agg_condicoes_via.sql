CREATE TEMP TABLE temp_fato_ocorrencia AS SELECT *
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/fato_ocorrencia/fato_ocorrencia.parquet') ;

CREATE TEMP TABLE temp_dim_tempo AS SELECT *
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/dim_tempo/dim_tempo.parquet');

CREATE TEMP TABLE temp_dim_condicao_metereologica AS SELECT *
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/dim_condicao_metereologica/dim_condicao_metereologica.parquet');

CREATE TEMP TABLE temp_dim_pista AS SELECT *
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/dim_pista/dim_pista.parquet');
    
CREATE TEMP TABLE temp_agg_condicoes_via AS
SELECT COALESCE((SELECT MAX(id) FROM "gold"."agg_condicoes_via"), 0) + ROW_NUMBER() OVER () AS id, source_data.*
FROM (
    SELECT
        t.ano,
        t.mes,
        t.dia,
        t.dia_semana,
        t.fase_dia,
        cm.condicao AS condicao_metereologica,
        p.sentido AS sentido_via,
        p.tracado AS tracado_via,
        p.tipo AS tipo_via,
        p.uso_solo AS solo_via,
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
        JOIN temp_dim_tempo AS t ON fato.sk_tempo = t.id
        JOIN temp_dim_condicao_metereologica AS cm ON fato.sk_condicao_metereologica = cm.id
        JOIN temp_dim_pista AS p ON fato.sk_pista = p.id
    GROUP BY
        t.ano,
        t.mes,
        t.dia,
        t.dia_semana,
        t.fase_dia,
        cm.condicao,
        p.sentido,
        p.tracado,
        p.tipo,
        p.uso_solo
) AS source_data;

MERGE INTO "gold"."agg_condicoes_via" AS target 
USING temp_agg_condicoes_via AS source 
    ON target.ano = source.ano 
    AND target.mes = source.mes 
    AND target.dia = source.dia 
    AND target.dia_semana = source.dia_semana 
    AND target.fase_dia = source.fase_dia 
    AND target.condicao_metereologica = source.condicao_metereologica 
    AND target.sentido_via = source.sentido_via 
    AND target.tracado_via = source.tracado_via 
    AND target.tipo_via = source.tipo_via 
    AND target.solo_via = source.solo_via

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
    condicao_metereologica,
    sentido_via,
    tracado_via,
    tipo_via,
    solo_via,
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
    source.condicao_metereologica,
    source.sentido_via,
    source.tracado_via,
    source.tipo_via,
    source.solo_via,
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
DROP TABLE IF EXISTS temp_dim_condicao_metereologica;
DROP TABLE IF EXISTS temp_dim_pista;
DROP TABLE IF EXISTS temp_agg_condicoes_via;