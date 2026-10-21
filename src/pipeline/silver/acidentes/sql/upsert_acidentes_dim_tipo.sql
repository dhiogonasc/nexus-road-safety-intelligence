CREATE TEMP TABLE temp_ocorrencias_tipo AS 
SELECT 
    COALESCE((SELECT MAX(id) FROM "silver"."dim_tipo"), 0) + ROW_NUMBER() OVER () AS id,
    source_data.id_carga,
    source_data.tipo
FROM (
    SELECT 
        max(id_carga) AS id_carga, 
        COALESCE(tipo_acidente :: VARCHAR, 'nao_informado') AS tipo
    FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet')
    GROUP BY COALESCE(tipo_acidente :: VARCHAR, 'nao_informado')
) AS source_data;

MERGE INTO "silver"."dim_tipo" AS target 
USING temp_ocorrencias_tipo AS source 
ON target.tipo = source.tipo

WHEN MATCHED AND target.id_carga <> source.id_carga THEN 
UPDATE SET 
    id_carga = source.id_carga,
    tipo = source.tipo

WHEN NOT MATCHED THEN 
INSERT (id, id_carga, tipo) 
VALUES (source.id, source.id_carga, source.tipo);

DROP TABLE IF EXISTS temp_ocorrencias_tipo;