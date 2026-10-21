CREATE TABLE IF NOT EXISTS "silver"."dim_causa" (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_carga VARCHAR,
    causa VARCHAR NOT NULL UNIQUE
);

BEGIN TRANSACTION;
TRY
    INSERT INTO "silver"."dim_causa" (id_carga, causa)
    SELECT id_carga, causa 
    FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/dim_causa/*.parquet')
    WHERE causa NOT IN (SELECT causa FROM "silver"."dim_causa");
CATCH
END TRY;
COMMIT;

CREATE TEMP TABLE temp_ocorrencias AS 
SELECT DISTINCT 
    id_carga, 
    COALESCE(causa_acidente :: VARCHAR, 'nao_informado') AS causa
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet');

MERGE INTO "silver"."dim_causa" AS target 
USING temp_ocorrencias AS source 
ON target.causa = source.causa

WHEN MATCHED AND target.id_carga <> source.id_carga THEN 
UPDATE SET 
    id_carga = source.id_carga,
    causa = source.causa

WHEN NOT MATCHED THEN 
INSERT (id_carga, causa) 
VALUES (source.id_carga, source.causa);

COPY "silver"."dim_causa" 
TO 's3://{settings.STORAGE_BUCKET}/{domain}/silver/dim_causa/' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);

DROP TABLE IF EXISTS temp_ocorrencias;

