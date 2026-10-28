INSERT INTO "silver"."dim_tipo"(id, tipo)
SELECT source.id, source.tipo
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "silver"."dim_tipo" AS target 
    WHERE target.id = source.id
);