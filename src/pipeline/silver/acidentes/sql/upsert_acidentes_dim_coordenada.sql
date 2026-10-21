CREATE TEMP TABLE temp_ocorrencias_coordenada AS 
SELECT 
    COALESCE((SELECT MAX(id) FROM "silver"."dim_coordenada"), 0) + ROW_NUMBER() OVER () AS id,
    source_data.id_carga,
    source_data.latitude,
    source_data.longitude
FROM (
    SELECT 
        max(id_carga) AS id_carga, 
        TRY_CAST(REPLACE(latitude :: VARCHAR, ',', '.') AS DOUBLE) AS latitude,
        TRY_CAST(REPLACE(longitude :: VARCHAR, ',', '.') AS DOUBLE) AS longitude
    FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet')
    GROUP BY 2, 3
) AS source_data;

MERGE INTO "silver"."dim_coordenada" AS target 
USING temp_ocorrencias_coordenada AS source 
ON target.latitude = source.latitude
AND target.longitude = source.longitude

WHEN MATCHED AND target.id_carga <> source.id_carga THEN 
UPDATE SET 
    id_carga = source.id_carga,
    latitude = source.latitude,
    longitude = source.longitude

WHEN NOT MATCHED THEN 
INSERT (id, id_carga, latitude, longitude) 
VALUES (source.id, source.id_carga, source.latitude, source.longitude);

DROP TABLE IF EXISTS temp_ocorrencias_coordenada;