INSERT INTO "silver"."dim_coordenada"(id, latitude, longitude)
SELECT source.id, source.latitude, source.longitude
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "silver"."dim_coordenada" AS target 
    WHERE target.id = source.id
);