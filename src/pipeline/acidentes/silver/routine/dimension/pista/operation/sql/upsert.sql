SELECT setval(
    'seq_dim_pista', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."dim_pista"), 0), 1)
);

CREATE TEMP TABLE temp_dim_pista AS 
SELECT 
    nextval('seq_dim_pista') AS id, 
    sentido, 
    tracado, 
    tipo, 
    solo
FROM (
    SELECT DISTINCT 
        sentido, 
        tracado, 
        tipo, 
        uso_solo as solo
    FROM "silver"."ultima_carga"
);

MERGE INTO "silver"."dim_pista" AS target 
USING temp_dim_pista AS source 
    ON target.sentido = source.sentido 
    AND target.tracado = source.tracado 
    AND target.tipo = source.tipo 
    AND target.solo = source.solo

WHEN NOT MATCHED THEN 
INSERT (
    id, 
    sentido, 
    tracado, 
    tipo, 
    solo
) 
VALUES (
    source.id, 
    source.sentido, 
    source.tracado, 
    source.tipo, 
    source.solo
);

DROP TABLE IF EXISTS temp_dim_localizacao;