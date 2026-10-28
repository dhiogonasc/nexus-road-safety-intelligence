SELECT setval(
    'seq_dim_coordenada', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."dim_coordenada"), 0), 1)
);

CREATE TEMP TABLE temp_dim_coordenada AS 
SELECT nextval('seq_dim_coordenada') AS id, latitude, longitude
FROM (
    SELECT DISTINCT latitude, longitude
    FROM "silver"."stg"
);

MERGE INTO "silver"."dim_coordenada" AS target 
USING temp_dim_coordenada AS source 
    ON target.latitude = source.latitude 
    AND target.longitude = source.longitude

WHEN NOT MATCHED THEN 
INSERT (id, latitude, longitude) 
VALUES (source.id, source.latitude, source.longitude);

DROP TABLE IF EXISTS temp_dim_coordenada;