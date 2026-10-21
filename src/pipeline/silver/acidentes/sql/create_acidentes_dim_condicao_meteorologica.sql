CREATE TABLE IF NOT EXISTS "silver"."dim_condicao_meteorologica" (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_carga VARCHAR,
    condicao_meteorologica VARCHAR NOT NULL UNIQUE
);

BEGIN TRANSACTION;
TRY
    INSERT INTO "silver"."dim_condicao_meteorologica" (id_carga, condicao_meteorologica)
    SELECT id_carga, condicao_meteorologica 
    FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/dim_condicao_meteorologica/*.parquet')
    WHERE condicao_meteorologica NOT IN (SELECT condicao_meteorologica FROM "silver"."dim_condicao_meteorologica");
CATCH
END TRY;
COMMIT;

CREATE TEMP TABLE temp_ocorrencias AS 
SELECT DISTINCT id_carga, COALESCE(condicao_meteorologica :: VARCHAR, 'nao_informado') AS condicao_meteorologica
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet');

MERGE INTO "silver"."dim_condicao_meteorologica" AS target 
USING temp_ocorrencias AS source 
ON target.condicao_meteorologica = source.condicao_meteorologica

WHEN MATCHED AND target.id_carga <> source.id_carga THEN 
UPDATE SET 
    id_carga = source.id_carga,
    condicao_meteorologica = source.condicao_meteorologica

WHEN NOT MATCHED THEN 
INSERT (id_carga, condicao_meteorologica) 
VALUES (source.id_carga, source.condicao_meteorologica);

COPY "silver"."dim_condicao_meteorologica" 
TO 's3://{settings.STORAGE_BUCKET}/{domain}/silver/dim_condicao_meteorologica/' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);

DROP TABLE IF EXISTS temp_ocorrencias;