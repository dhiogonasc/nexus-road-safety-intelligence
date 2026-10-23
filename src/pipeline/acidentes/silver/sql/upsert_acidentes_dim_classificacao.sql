CREATE TEMP TABLE temp_dim_classificacao AS 
SELECT 
    COALESCE((SELECT MAX(id) FROM "silver"."dim_classificacao"), 0) + ROW_NUMBER() OVER () AS id,
    source_data.classificacao
FROM (
    SELECT COALESCE(classificacao_acidente :: VARCHAR, 'nao_informado') AS classificacao
    FROM 
        read_parquet(
            's3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet', 
            hive_partitioning = true
        )
    WHERE data_carga = (
        SELECT MAX(data_carga) 
        FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias_log/**/*.parquet')
    )
) AS source_data;

MERGE INTO "silver"."dim_classificacao" AS target 
USING temp_dim_classificacao AS source 
ON target.classificacao = source.classificacao

WHEN NOT MATCHED THEN 
INSERT (id, classificacao) 
VALUES (source.id, source.classificacao);

DROP TABLE IF EXISTS temp_dim_classificacao;