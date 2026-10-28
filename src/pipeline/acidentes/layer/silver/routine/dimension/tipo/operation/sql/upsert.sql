SELECT setval(
    'seq_dim_tipo', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."dim_tipo"), 0), 1)
);

CREATE TEMP TABLE temp_dim_tipo AS 
SELECT nextval('seq_dim_tipo') AS id, tipo
FROM (
    SELECT DISTINCT tipo_acidente AS tipo
    FROM "silver"."stg"
);

MERGE INTO "silver"."dim_tipo" AS target 
USING temp_dim_tipo AS source 
    ON target.tipo = source.tipo

WHEN NOT MATCHED THEN 
INSERT (id, tipo) 
VALUES (source.id, source.tipo);

DROP TABLE IF EXISTS temp_dim_tipo;