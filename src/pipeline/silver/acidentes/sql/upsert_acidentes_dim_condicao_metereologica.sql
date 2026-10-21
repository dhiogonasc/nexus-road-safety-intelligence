CREATE TEMP TABLE temp_ocorrencias_condicao_metereologica AS 
SELECT 
    COALESCE((SELECT MAX(id) FROM "silver"."dim_condicao_metereologica"), 0) + ROW_NUMBER() OVER () AS id,
    source_data.id_carga,
    source_data.condicao
FROM (
    SELECT 
        max(id_carga) AS id_carga, 
        COALESCE(condicao_metereologica :: VARCHAR, 'nao_informado') AS condicao
    FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet')
    GROUP BY COALESCE(condicao_metereologica :: VARCHAR, 'nao_informado')
) AS source_data;

MERGE INTO "silver"."dim_condicao_metereologica" AS target 
USING temp_ocorrencias_condicao_metereologica AS source 
ON target.condicao = source.condicao

WHEN MATCHED AND target.id_carga <> source.id_carga THEN 
UPDATE SET 
    id_carga = source.id_carga,
    condicao = source.condicao

WHEN NOT MATCHED THEN 
INSERT (id, id_carga, condicao) 
VALUES (source.id, source.id_carga, source.condicao);

DROP TABLE IF EXISTS temp_ocorrencias_condicao_metereologica;