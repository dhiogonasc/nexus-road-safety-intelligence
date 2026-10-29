SELECT setval(
    'seq_dim_pista', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."dim_pista"), 0), 1)
);

CREATE TEMP TABLE temp_dim_pista AS 
SELECT 
    tracado,
    tipo
FROM (
    SELECT DISTINCT 
        tracado_via AS tracado, 
        tipo_pista AS tipo
    FROM "silver"."stg"
);

MERGE INTO "silver"."dim_pista" AS target 
USING temp_dim_pista AS source 
    AND target.tracado = source.tracado 
    AND target.tipo = source.tipo 

WHEN NOT MATCHED THEN 
INSERT (
    id, 
    tracado, 
    tipo
) 
VALUES (
    nextval('seq_dim_pista'),
    source.tracado, 
    source.tipo
);

DROP TABLE IF EXISTS temp_dim_pista;