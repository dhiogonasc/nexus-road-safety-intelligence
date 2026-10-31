SELECT setval(
    'seq_dim_tempo', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."dim_tempo"), 0), 1)
);

CREATE TEMP TABLE temp_dim_tempo AS 
SELECT 
    data_hora,
    ano, 
    mes, 
    dia, 
    hora,
    dia_semana, 
    fase_dia
FROM (
    SELECT DISTINCT 
        data_hora,
        ano, 
        mes, 
        dia, 
        hora,
        dia_semana, 
        fase_dia
    FROM "silver"."stg_ocorrencia"
);

MERGE INTO "silver"."dim_tempo" AS target 
USING temp_dim_tempo AS source 
    ON target.data_hora = source.data_hora 
    AND target.dia_semana = source.dia_semana 
    AND target.fase_dia = source.fase_dia

WHEN NOT MATCHED THEN 
INSERT (
    id, 
    data_hora, 
    ano, 
    mes, 
    dia, 
    hora, 
    dia_semana, 
    fase_dia
) 
VALUES (
    nextval('seq_dim_tempo'),
    source.data_hora, 
    source.ano, 
    source.mes, 
    source.dia, 
    source.hora, 
    source.dia_semana, 
    source.fase_dia
);

DROP TABLE IF EXISTS temp_dim_tempo;