SELECT setval(
    'seq_dim_categoria', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."dim_categoria"), 0), 1)
);

CREATE TEMP TABLE temp_dim_categoria AS 
SELECT 
    tipo,
    causa,
    classificacao
FROM (
    SELECT DISTINCT 
        tipo,
        causa,
        classificacao
    FROM "silver"."stg_ocorrencias"
);

MERGE INTO "silver"."dim_categoria" AS target 
USING temp_dim_categoria AS source 
    ON target.tipo = source.tipo
    AND target.causa = source.causa
    AND target.classificacao = source.classificacao

WHEN NOT MATCHED THEN 
INSERT (
    id, 
    tipo,
    causa,
    classificacao
) 
VALUES (
    nextval('seq_dim_categoria'),
    source.tipo,
    source.causa,
    source.classificacao
);

DROP TABLE IF EXISTS temp_dim_categoria;