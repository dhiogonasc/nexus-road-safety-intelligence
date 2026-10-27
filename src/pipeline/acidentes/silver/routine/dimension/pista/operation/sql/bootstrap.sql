INSERT INTO "silver"."dim_pista"(
    id,
    sentido,
    tracado,
    tipo,
    uso_solo
)
SELECT 
    source.id,
    source.sentido,
    source.tracado,
    source.tipo,
    source.uso_solo
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "silver"."dim_pista" AS target 
    WHERE target.id = source.id
);