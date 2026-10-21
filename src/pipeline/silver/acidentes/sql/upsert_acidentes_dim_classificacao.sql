CREATE TEMP TABLE temp_ocorrencias_classificacao AS 
SELECT DISTINCT 
    id_carga, 
    COALESCE(classificacao_acidente :: VARCHAR, 'nao_informado') AS classificacao,
    COALESCE((SELECT MAX(id) FROM "silver"."dim_classificacao"), 0) + ROW_NUMBER() OVER () AS id
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet');

MERGE INTO "silver"."dim_classificacao" AS target 
USING temp_ocorrencias_classificacao AS source 
ON target.classificacao = source.classificacao

WHEN MATCHED AND target.id_carga <> source.id_carga THEN 
UPDATE SET 
    id_carga = source.id_carga,
    classificacao = source.classificacao

WHEN NOT MATCHED THEN 
INSERT (id, id_carga, classificacao) 
VALUES (source.id, source.id_carga, source.classificacao);

DROP TABLE IF EXISTS temp_ocorrencias_classificacao;