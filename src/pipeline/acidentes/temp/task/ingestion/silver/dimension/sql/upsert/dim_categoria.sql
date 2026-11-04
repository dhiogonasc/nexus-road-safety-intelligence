SELECT setval(
    'seq_dim_categoria', 
    COALESCE((SELECT MAX(id) FROM "silver"."dim_categoria"), 1)
);

MERGE INTO "silver"."dim_categoria" AS target 
USING (
    SELECT DISTINCT 
        tipo,
        causa,
        classificacao
    FROM "silver"."stg_ocorrencias"
) AS source 
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
