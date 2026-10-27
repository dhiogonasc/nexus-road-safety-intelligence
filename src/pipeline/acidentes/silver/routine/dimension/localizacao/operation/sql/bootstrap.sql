INSERT INTO "silver"."dim_localizacao"(
    id,
    uf, br, km, uop,
    municipio,
    regional,
    delegacia
)
SELECT 
    source.id, 
    source.uf, 
    source.br, 
    source.km, 
    source.uop, 
    source.municipio, 
    source.regional, 
    source.delegacia
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "silver"."dim_localizacao" AS target 
    WHERE target.id = source.id
);