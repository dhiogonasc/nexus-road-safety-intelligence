INSERT INTO "silver"."dim_condicao_metereologica"(id, condicao)
SELECT source.id, source.condicao
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "silver"."dim_condicao_metereologica" AS target 
    WHERE target.id = source.id
);