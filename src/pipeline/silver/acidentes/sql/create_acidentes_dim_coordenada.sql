CREATE TABLE IF NOT EXISTS "silver"."dim_coordenada" (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_carga VARCHAR,
    km DOUBLE NOT NULL,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,

    CONSTRAINT uk_dim_coordenada UNIQUE (km, latitude, longitude)
);

BEGIN TRANSACTION;
TRY
    INSERT INTO "silver"."dim_coordenada" (
        id_carga, km, latitude, longitude )
    SELECT id_carga, km, latitude, longitude 
    FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/dim_coordenada/*.parquet')
    WHERE (km, latitude, longitude) NOT IN (SELECT km, latitude, longitude FROM "silver"."dim_coordenada");
CATCH
END TRY;
COMMIT;

CREATE TEMP TABLE temp_ocorrencias AS 
SELECT DISTINCT 
    id_carga, 
    TRY_CAST(REPLACE(km :: VARCHAR, ',', '.') AS DOUBLE) AS km,
    TRY_CAST(REPLACE(latitude :: VARCHAR, ',', '.') AS DOUBLE) AS latitude,
    TRY_CAST(REPLACE(longitude :: VARCHAR, ',', '.') AS DOUBLE) AS longitude
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet');

MERGE INTO "silver"."dim_coordenada" AS target 
USING temp_ocorrencias AS source 
ON target.km = source.km
AND target.latitude = source.latitude
AND target.longitude = source.longitude

WHEN MATCHED AND target.id_carga <> source.id_carga THEN 
UPDATE SET 
    id_carga = source.id_carga
    km = source.km
    latitude = source.latitude
    longitude = source.longitude

WHEN NOT MATCHED THEN 
INSERT (id_carga, km, latitude, longitude) 
VALUES (source.id_carga, source.km, source.latitude, source.longitude);

COPY "silver"."dim_coordenada" 
TO 's3://{settings.STORAGE_BUCKET}/{domain}/silver/dim_coordenada/' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);

DROP TABLE IF EXISTS temp_ocorrencias;