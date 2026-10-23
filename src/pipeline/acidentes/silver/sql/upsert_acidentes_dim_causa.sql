CREATE TEMP TABLE temp_dim_causa AS 
SELECT 
    COALESCE((SELECT MAX(id) FROM "silver"."dim_causa"), 0) + ROW_NUMBER() OVER () AS id,
    source_data.causa
FROM (
    SELECT COALESCE(causa_acidente :: VARCHAR, 'nao_informado') AS causa
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

MERGE INTO "silver"."dim_causa" AS target 
USING temp_dim_causa AS source 
ON target.causa = source.causa

WHEN NOT MATCHED THEN 
INSERT (id, causa) 
VALUES (source.id, source.causa);

DROP TABLE IF EXISTS temp_dim_causa;