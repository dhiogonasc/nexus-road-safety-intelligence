CREATE TABLE IF NOT EXISTS "silver"."dim_tipo" (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_carga VARCHAR,
    tipo VARCHAR NOT NULL UNIQUE
);

BEGIN TRANSACTION;
TRY
    INSERT INTO "silver"."dim_tipo" (id_carga, tipo)
    SELECT id_carga, tipo 
    FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/dim_tipo/*.parquet')
    WHERE tipo NOT IN (SELECT tipo FROM "silver"."dim_tipo");
CATCH
END TRY;
COMMIT;

CREATE TEMP TABLE temp_ocorrencias AS 
SELECT DISTINCT id_carga, COALESCE(tipo_acidente :: VARCHAR, 'nao_informado') AS tipo
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet');

MERGE INTO "silver"."dim_tipo" AS target 
USING temp_ocorrencias AS source 
ON target.tipo = source.tipo

WHEN MATCHED AND target.id_carga <> source.id_carga THEN 
UPDATE SET 
    id_carga = source.id_carga
    tipo = source.tipo

WHEN NOT MATCHED THEN 
INSERT (id_carga, tipo) 
VALUES (source.id_carga, source.tipo);

COPY "silver"."dim_tipo" 
TO 's3://{settings.STORAGE_BUCKET}/{domain}/silver/dim_tipo/' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);

DROP TABLE IF EXISTS temp_ocorrencias;