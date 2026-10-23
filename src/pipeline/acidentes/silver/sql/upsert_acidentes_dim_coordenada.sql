CREATE TEMP TABLE temp_dim_coordenada AS 
SELECT 
    COALESCE((SELECT MAX(id) FROM "silver"."dim_coordenada"), 0) + ROW_NUMBER() OVER () AS id,
    source_data.latitude,
    source_data.longitude
FROM (
    SELECT 
        TRY_CAST(REPLACE(latitude :: VARCHAR, ',', '.') AS DOUBLE) AS latitude,
        TRY_CAST(REPLACE(longitude :: VARCHAR, ',', '.') AS DOUBLE) AS longitude
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

MERGE INTO "silver"."dim_coordenada" AS target 
USING temp_dim_coordenada AS source 
ON target.latitude = source.latitude
AND target.longitude = source.longitude

WHEN NOT MATCHED THEN 
INSERT (id, latitude, longitude) 
VALUES (source.id, source.latitude, source.longitude);

DROP TABLE IF EXISTS temp_dim_coordenada;