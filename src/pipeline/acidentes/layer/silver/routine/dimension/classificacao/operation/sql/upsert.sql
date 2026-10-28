SELECT setval(
    'seq_dim_classificacao', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."dim_classificacao"), 0), 1)
);

CREATE TEMP TABLE temp_dim_classificacao AS 
SELECT nextval('seq_dim_classificacao') AS id, classificacao
FROM (
    SELECT DISTINCT classificacao_acidente AS classificacao
    FROM "silver"."ultima_carga"
);

MERGE INTO "silver"."dim_classificacao" AS target 
USING temp_dim_classificacao AS source 
    ON target.classificacao = source.classificacao

WHEN NOT MATCHED THEN 
INSERT (id, classificacao) 
VALUES (source.id, source.classificacao);

DROP TABLE IF EXISTS temp_dim_classificacao;