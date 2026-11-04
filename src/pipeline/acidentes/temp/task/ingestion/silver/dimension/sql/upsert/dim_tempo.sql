SELECT setval(
    'seq_dim_tempo', 
    COALESCE((SELECT MAX(id) FROM "silver"."dim_tempo"), 1)
);

MERGE INTO "silver"."dim_tempo" AS target 
USING (
    SELECT DISTINCT 
        ano, 
        mes, 
        semana,
        dia_semana, 
        fase_dia,
        mes_str, 
        dia_semana_str, 
        fase_dia_str
    FROM "silver"."stg_ocorrencias"
) AS source 
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
    fase_dia,
    mes_str, 
    dia_semana_str, 
    fase_dia_str
) 
VALUES (
    nextval('seq_dim_tempo'),
    source.ano, 
    source.mes, 
    source.semana, 
    source.dia_semana, 
    source.fase_dia,
    source.mes_str, 
    source.dia_semana_str, 
    source.fase_dia_str
);
