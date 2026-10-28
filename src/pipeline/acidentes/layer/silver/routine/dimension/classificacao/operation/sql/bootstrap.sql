INSERT INTO "silver"."dim_classificacao"(id, classificacao)
SELECT source.id, source.classificacao
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "silver"."dim_classificacao" AS target 
    WHERE target.id = source.id
);