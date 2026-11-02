SELECT setval(
    'seq_dim_tempo', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."dim_tempo"), 0), 1)
);

CREATE TEMP TABLE temp_dim_tempo AS 
SELECT 
    ano, 
    mes, 
    semana,
    dia_semana, 
    fase_dia
FROM (
    SELECT DISTINCT 
        ano, 
        mes, 
        semana,
        dia_semana, 
        fase_dia
    FROM "silver"."stg_ocorrencias"
);

MERGE INTO "silver"."dim_tempo" AS target 
USING temp_dim_tempo AS source 
    ON target.ano = source.ano 
    AND target.mes = source.mes 
    AND target.semana = source.semana 
    AND target.dia_semana = source.dia_semana 
    AND target.fase_dia = source.fase_dia

WHEN NOT MATCHED THEN 
INSERT (
    id, 
    ano, 
    mes, 
    semana,
    dia_semana, 
    fase_dia
) 
VALUES (
    nextval('seq_dim_tempo'),
    source.ano, 
    source.mes, 
    source.semana, 
    source.dia_semana, 
    source.fase_dia
);

DROP TABLE IF EXISTS temp_dim_tempo;