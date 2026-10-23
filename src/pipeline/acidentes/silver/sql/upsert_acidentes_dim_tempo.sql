CREATE TEMP TABLE temp_dim_tempo AS 
SELECT 
    COALESCE((SELECT MAX(id) FROM "silver"."dim_tempo"), 0) + ROW_NUMBER() OVER () AS id,
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
            COALESCE(dia_semana :: VARCHAR, 'nao_informado') AS dia_semana,
            COALESCE(fase_dia :: VARCHAR, 'nao_informado') AS fase_dia,
            TRY_CAST(data_inversa AS DATE) AS base_data,
            TRY_CAST(horario AS TIME) AS base_hora
        FROM 
            read_parquet(
                's3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet', 
                hive_partitioning = true
            )
        WHERE data_inversa IS NOT NULL 
            AND horario IS NOT NULL
            AND data_carga = (
                SELECT MAX(data_carga) 
                FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias_log/**/*.parquet')
            )
    ),
    formatted_tempo AS (
        SELECT
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
        data_hora,
        ano,
        mes,
        dia,
        hora,
        dia_semana,
        fase_dia
    FROM formatted_tempo
) AS source_data;

MERGE INTO "silver"."dim_tempo" AS target 
USING temp_dim_tempo AS source 
ON target.data_hora = source.data_hora
AND target.dia_semana = source.dia_semana
AND target.fase_dia = source.fase_dia

WHEN NOT MATCHED THEN 
INSERT (
    id, 
    data_hora, 
    ano, mes, 
    dia, hora, 
    dia_semana, 
    fase_dia
) 
VALUES (
    source.id, 
    source.data_hora, 
    source.ano, 
    source.mes, 
    source.dia, 
    source.hora, 
    source.dia_semana, 
    source.fase_dia
);

DROP TABLE IF EXISTS temp_dim_tempo;