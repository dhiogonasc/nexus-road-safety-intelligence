INSERT INTO "silver"."dim_causa"(id, causa)
SELECT source.id, source.causa
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "silver"."dim_causa" AS target 
    WHERE target.id = source.id
);