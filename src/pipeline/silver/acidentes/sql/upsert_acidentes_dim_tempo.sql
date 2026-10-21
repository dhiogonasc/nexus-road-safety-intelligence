CREATE TEMP TABLE temp_ocorrencias_tempo AS 
SELECT 
    COALESCE((SELECT MAX(id) FROM "silver"."dim_tempo"), 0) + ROW_NUMBER() OVER () AS id,
    source_data.id_carga,
    source_data.data_hora,
    source_data.ano,
    source_data.mes,
    source_data.dia,
    source_data.hora,
    source_data.dia_semana,
    source_data.fase_dia
FROM (
    WITH base_tempo AS (
        SELECT 
            id_carga,
            COALESCE(dia_semana :: VARCHAR, 'nao_informado') AS dia_semana,
            COALESCE(fase_dia :: VARCHAR, 'nao_informado') AS fase_dia,
            TRY_CAST(data_inversa AS DATE) AS base_data,
            TRY_CAST(horario AS TIME) AS base_hora
        FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet')
        WHERE data_inversa IS NOT NULL 
        AND horario IS NOT NULL
    ),
    formatted_tempo AS (
        SELECT
            id_carga,
            dia_semana,
            fase_dia,
            (base_data + base_hora) AS data_hora,
            EXTRACT(YEAR FROM base_data) AS ano,
            EXTRACT(MONTH FROM base_data) AS mes,
            EXTRACT(DAY FROM base_data) AS dia,
            EXTRACT(HOUR FROM base_hora) AS hora
        FROM base_tempo
    )
    SELECT 
        MAX(id_carga) AS id_carga, 
        data_hora,
        ano,
        mes,
        dia,
        hora,
        dia_semana,
        fase_dia
    FROM formatted_tempo
    GROUP BY 2, 3, 4, 5, 6, 7, 8
) AS source_data;

MERGE INTO "silver"."dim_tempo" AS target 
USING temp_ocorrencias_tempo AS source 
ON target.ano = source.ano
AND target.mes = source.mes
AND target.dia = source.dia
AND target.hora = source.hora
AND target.dia_semana = source.dia_semana
AND target.fase_dia = source.fase_dia
AND target.data_hora = source.data_hora

WHEN MATCHED AND target.id_carga <> source.id_carga THEN 
UPDATE SET 
    id_carga = source.id_carga,
    data_hora = source.data_hora,
    ano = source.ano,
    mes = source.mes,
    dia = source.dia,
    hora = source.hora,
    dia_semana = source.dia_semana,
    fase_dia = source.fase_dia

WHEN NOT MATCHED THEN 
INSERT (
    id, 
    id_carga, 
    data_hora, 
    ano, mes, 
    dia, hora, 
    dia_semana, 
    fase_dia
) 
VALUES (
    source.id, 
    source.id_carga, 
    source.data_hora, 
    source.ano, 
    source.mes, 
    source.dia, 
    source.hora, 
    source.dia_semana, 
    source.fase_dia
);

DROP TABLE IF EXISTS temp_ocorrencias_tempo;