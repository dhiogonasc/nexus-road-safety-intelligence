INSERT INTO "silver"."dim_pista"(
    id,
    tracado,
    tipo
)
SELECT 
    source.id,
    source.tracado,
    source.tipo
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "silver"."dim_pista" AS target 
    WHERE target.id = source.id
);