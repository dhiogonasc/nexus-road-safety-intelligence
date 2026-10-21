CREATE TABLE IF NOT EXISTS "silver"."dim_classificacao" (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_carga VARCHAR,
    classificacao VARCHAR NOT NULL UNIQUE
);

BEGIN TRANSACTION;
TRY
    INSERT INTO "silver"."dim_classificacao" (id_carga, classificacao)
    SELECT id_carga, classificacao 
    FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/dim_classificacao/*.parquet')
    WHERE classificacao NOT IN (SELECT classificacao FROM "silver"."dim_classificacao");
CATCH
END TRY;
COMMIT;

CREATE TEMP TABLE temp_ocorrencias AS 
SELECT DISTINCT id_carga, COALESCE(classificacao_acidente :: VARCHAR, 'nao_informado') AS classificacao
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet');

MERGE INTO "silver"."dim_classificacao" AS target 
USING temp_ocorrencias AS source 
ON target.classificacao = source.classificacao

WHEN MATCHED AND target.id_carga <> source.id_carga THEN 
UPDATE SET 
    id_carga = source.id_carga
    classificacao = source.classificacao

WHEN NOT MATCHED THEN 
INSERT (id_carga, classificacao) 
VALUES (source.id_carga, source.classificacao);

DROP TABLE IF EXISTS temp_ocorrencias;