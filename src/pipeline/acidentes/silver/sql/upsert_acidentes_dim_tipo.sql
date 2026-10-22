CREATE TEMP TABLE temp_dim_tipo AS 
SELECT 
    COALESCE((SELECT MAX(id) FROM "silver"."dim_tipo"), 0) + ROW_NUMBER() OVER () AS id,
    source_data.tipo
FROM (
    SELECT COALESCE(tipo_acidente :: VARCHAR, 'nao_informado') AS tipo
    FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet')
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY COALESCE(tipo_acidente :: VARCHAR, 'nao_informado')
        ORDER BY data_carga DESC
    ) = 1
) AS source_data;

MERGE INTO "silver"."dim_tipo" AS target 
USING temp_dim_tipo AS source 
ON target.tipo = source.tipo

WHEN NOT MATCHED THEN 
INSERT (id, tipo) 
VALUES (source.id, source.tipo);

DROP TABLE IF EXISTS temp_dim_tipo;