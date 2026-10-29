INSERT INTO "silver"."dim_categoria"(
    id, 
    classificacao,
    causa,
    tipo
)
SELECT 
    source.id, 
    source.condicao
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "silver"."dim_categoria" AS target 
    WHERE target.id = source.id
);