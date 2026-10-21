CREATE TEMP TABLE temp_ocorrencias_pista AS 
SELECT 
    COALESCE((SELECT MAX(id) FROM "silver"."dim_pista"), 0) + ROW_NUMBER() OVER () AS id,
    source_data.id_carga,
    source_data.sentido,
    source_data.tracado,
    source_data.tipo,
    source_data.uso_solo
FROM (
    SELECT 
        MAX(id_carga) AS id_carga, 
        COALESCE(sentido_via :: VARCHAR, 'nao_informado') AS sentido,
        COALESCE(tracado_via :: VARCHAR, 'nao_informado') AS tracado,
        COALESCE(tipo_pista :: VARCHAR, 'nao_informado') AS tipo,
        COALESCE(uso_solo :: VARCHAR, 'nao_informado') AS uso_solo
    FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet')
    GROUP BY 2, 3, 4, 5
) AS source_data;

MERGE INTO "silver"."dim_pista" AS target 
USING temp_ocorrencias_pista AS source 
ON target.sentido = source.sentido
AND target.tracado = source.tracado
AND target.tipo = source.tipo
AND target.uso_solo = source.uso_solo

WHEN MATCHED AND target.id_carga <> source.id_carga THEN 
UPDATE SET 
    id_carga = source.id_carga,
    sentido = source.sentido,
    tracado = source.tracado,
    tipo = source.tipo,
    uso_solo = source.uso_solo

WHEN NOT MATCHED THEN 
INSERT (
    id,
    id_carga, 
    sentido, 
    tracado, 
    tipo, 
    uso_solo
) 
VALUES (
    source.id,
    source.id_carga, 
    source.sentido, 
    source.tracado, 
    source.tipo, 
    source.uso_solo
);

DROP TABLE IF EXISTS temp_ocorrencias_pista;