CREATE TEMP TABLE temp_ocorrencias_causa AS 
SELECT DISTINCT 
    id_carga,
    data_carga,
    COALESCE(causa_acidente :: VARCHAR, 'nao_informado') AS causa
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet');

MERGE INTO "silver"."dim_causa" AS target 
USING temp_ocorrencias_causa AS source 
ON target.causa = source.causa

WHEN MATCHED AND target.id_carga <> source.id_carga THEN 
UPDATE SET 
    id_carga = source.id_carga,
    data_carga = soruce.data_carga
    causa = source.causa

WHEN NOT MATCHED THEN 
INSERT (id_carga, causa) 
VALUES (source.id_carga, source.data_carga, source.causa);

DROP TABLE IF EXISTS temp_ocorrencias_causa;

