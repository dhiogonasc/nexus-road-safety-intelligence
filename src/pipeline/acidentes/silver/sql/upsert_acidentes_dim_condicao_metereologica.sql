CREATE TEMP TABLE temp_dim_condicao_metereologica AS 
SELECT 
    COALESCE((SELECT MAX(id) FROM "silver"."dim_condicao_metereologica"), 0) + ROW_NUMBER() OVER () AS id,
    source_data.condicao
FROM (
    SELECT COALESCE(condicao_metereologica :: VARCHAR, 'nao_informado') AS condicao
    FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet')
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY COALESCE(condicao_metereologica :: VARCHAR, 'nao_informado') 
        ORDER BY data_carga DESC
    ) = 1
) AS source_data;

MERGE INTO "silver"."dim_condicao_metereologica" AS target 
USING temp_dim_condicao_metereologica AS source 
ON target.condicao = source.condicao

WHEN NOT MATCHED THEN 
INSERT (id, condicao) 
VALUES (source.id, source.condicao);

DROP TABLE IF EXISTS temp_dim_condicao_metereologica;