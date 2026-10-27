SELECT setval(
    'seq_dim_causa', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."dim_causa"), 0), 1)
);

CREATE TEMP TABLE temp_dim_causa AS 
SELECT nextval('seq_dim_causa') AS id, causa
FROM (
    SELECT DISTINCT causa_acidente AS causa
    FROM "silver"."ultima_carga"
);

MERGE INTO "silver"."dim_causa" AS target 
USING temp_dim_causa AS source 
    ON target.causa = source.causa

WHEN NOT MATCHED THEN 
INSERT (id, causa) 
VALUES (source.id, source.causa);

DROP TABLE IF EXISTS temp_dim_causa;