INSERT INTO "silver"."dim_local"(
    id,
    uf, 
    br, 
    km,
    sentido,
    municipio,
    area,
    latitude,
    longitude
)
SELECT 
    source.id,
    source.uf, 
    source.br, 
    source.km,
    source.sentido,
    source.municipio,
    source.area,
    source.latitude,
    source.longitude
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "silver"."dim_local" AS target 
    WHERE target.id = source.id
);