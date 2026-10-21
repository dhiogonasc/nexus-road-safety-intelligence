INSERT INTO "silver"."dim_causa" (id_carga, causa)
SELECT id_carga, causa 
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/dim_causa/*.parquet')
WHERE causa NOT IN (SELECT causa FROM "silver"."dim_causa");