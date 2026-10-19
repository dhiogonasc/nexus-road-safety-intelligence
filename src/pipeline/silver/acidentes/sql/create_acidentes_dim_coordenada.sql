CREATE OR REPLACE TABLE "silver"."dim_coordenada" AS 
WITH base AS (
    SELECT DISTINCT 
        TRY_CAST(REPLACE(km :: VARCHAR, ',', '.') AS DOUBLE) AS km,
        TRY_CAST(REPLACE(latitude :: VARCHAR, ',', '.') AS DOUBLE) AS latitude,
        TRY_CAST(REPLACE(longitude :: VARCHAR, ',', '.') AS DOUBLE) AS longitude
    FROM "bronze"."ocorrencias"
)
SELECT 
    ROW_NUMBER() OVER (ORDER BY km, latitude, longitude) AS id,
    km,
    latitude,
    longitude
FROM base;