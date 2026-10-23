CREATE TEMP TABLE temp_dim_pista AS 
SELECT 
    COALESCE((SELECT MAX(id) FROM "silver"."dim_pista"), 0) + ROW_NUMBER() OVER () AS id,
    source_data.sentido,
    source_data.tracado,
    source_data.tipo,
    source_data.uso_solo
FROM (
    SELECT 
        COALESCE(sentido_via :: VARCHAR, 'nao_informado') AS sentido,
        COALESCE(tracado_via :: VARCHAR, 'nao_informado') AS tracado,
        COALESCE(tipo_pista :: VARCHAR, 'nao_informado') AS tipo,
        COALESCE(uso_solo :: VARCHAR, 'nao_informado') AS uso_solo
    FROM 
        read_parquet(
            's3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet', 
            hive_partitioning = true
        )
    WHERE data_carga = (
        SELECT MAX(data_carga) 
        FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias_log/**/*.parquet')
    )
) AS source_data;

MERGE INTO "silver"."dim_pista" AS target 
USING temp_dim_pista AS source 
ON target.sentido = source.sentido
AND target.tracado = source.tracado
AND target.tipo = source.tipo
AND target.uso_solo = source.uso_solo

WHEN NOT MATCHED THEN 
INSERT (
    id,
    sentido, 
    tracado, 
    tipo, 
    uso_solo
) 
VALUES (
    source.id,
    source.sentido, 
    source.tracado, 
    source.tipo, 
    source.uso_solo
);

DROP TABLE IF EXISTS temp_dim_pista;