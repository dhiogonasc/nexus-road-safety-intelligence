INSERT INTO "silver"."dim_jurisdicao"(
    id, 
    uop,
    regional,
    delegacia
)
SELECT 
    source.id, 
    source.uop,
    source.regional,
    source.delegacia
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "silver"."dim_jursdicao" AS target 
    WHERE target.id = source.id
);