SELECT setval(
    'seq_dim_categoria', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."dim_categoria"), 0), 1)
);

CREATE TEMP TABLE temp_dim_categoria AS 
SELECT 
    classificacao,
    causa,
    tipo
FROM (
    SELECT DISTINCT 
        classificacao_acidente AS classificacao,
        causa_acidente AS causa,
        tipo_acidente AS tipo
    FROM "silver"."stg_ocorrencia"
);

MERGE INTO "silver"."dim_categoria" AS target 
USING temp_dim_categoria AS source 
    ON target.classificacao = source.classificacao
    AND target.causa = source.causa
    AND target.tipo = source.tipo

WHEN NOT MATCHED THEN 
INSERT (
    id, 
    classificacao,
    causa,
    tipo
) 
VALUES (
    nextval('seq_dim_categoria'),
    source.classificacao,
    source.causa,
    source.tipo
);

DROP TABLE IF EXISTS temp_dim_categoria;