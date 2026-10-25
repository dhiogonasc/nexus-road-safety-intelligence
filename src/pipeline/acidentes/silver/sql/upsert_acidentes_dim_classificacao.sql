SELECT setval(
    'seq_dim_classificacao', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."dim_classificacao"), 0), 1)
);

CREATE TEMP TABLE temp_dim_classificacao AS 
SELECT 
    nextval('seq_dim_classificacao') AS id,
    source_data.classificacao
FROM (
    SELECT classificacao_acidente AS classificacao
    FROM "silver"."last_charged"
) AS source_data;

MERGE INTO "silver"."dim_classificacao" AS target 
USING temp_dim_classificacao AS source 
ON target.classificacao = source.classificacao

WHEN NOT MATCHED THEN 
INSERT (id, classificacao) 
VALUES (source.id, source.classificacao);

DROP TABLE IF EXISTS temp_dim_classificacao;