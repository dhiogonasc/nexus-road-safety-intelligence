CREATE TABLE IF NOT EXISTS "silver"."dim_tempo" (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_carga VARCHAR,
    data_hora TIMESTAMP,
    ano INTEGER,
    mes INTEGER,
    dia INTEGER,
    hora INTEGER,
    dia_semana VARCHAR,
    fase_dia VARCHAR
);

BEGIN TRANSACTION;
TRY
    INSERT INTO "silver"."dim_tempo" (
        id_carga, data_hora, 
        ano, mes, dia, hora, 
        dia_semana, fase_dia
    )
    SELECT 
        id_carga, data_hora, 
        ano, mes, dia, hora, 
        dia_semana, fase_dia
    FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/dim_tempo/*.parquet')
    WHERE (
        id_carga, data_hora, 
        ano, mes, dia, hora, 
        dia_semana, fase_dia
    ) NOT IN (
        SELECT 
            id_carga, data_hora, 
            ano, mes, dia, hora, 
            dia_semana, fase_dia 
        FROM "silver"."dim_tempo"
    );
CATCH
END TRY;
COMMIT;

CREATE TEMP TABLE temp_ocorrencias AS 
WITH base_tempo AS (
    SELECT DISTINCT
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
    id_carga,
    data_hora,
    ano,
    mes,
    dia,
    hora,
    dia_semana,
    fase_dia
FROM formatted_tempo;


MERGE INTO "silver"."dim_tempo" AS target 
USING temp_ocorrencias AS source 
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
        id_carga, data_hora, 
        ano, mes, dia, hora, 
        dia_semana, fase_dia
    ) 
    VALUES ( 
        source.id_carga, 
        source.data_hora, 
        source.ano, 
        source.mes, 
        source.dia, 
        source.hora, 
        source.dia_semana, 
        source.fase_dia
    );

COPY "silver"."dim_tempo" 
TO 's3://{settings.STORAGE_BUCKET}/{domain}/silver/dim_tempo/' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);

DROP TABLE IF EXISTS temp_ocorrencias;