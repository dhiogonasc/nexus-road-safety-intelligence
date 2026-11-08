INSERT INTO "silver"."dim_categoria"(
    id, 
    tipo,
    causa,
    classificacao
)
SELECT 
    source.id, 
    source.tipo,
    source.causa,
    source.classificacao
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "silver"."dim_categoria" AS target 
    WHERE target.id = source.id
);