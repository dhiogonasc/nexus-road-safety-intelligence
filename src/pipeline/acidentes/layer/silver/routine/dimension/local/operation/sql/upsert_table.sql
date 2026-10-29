SELECT setval(
    'seq_dim_local', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."dim_local"), 0), 1)
);

CREATE TEMP TABLE temp_dim_local AS 
SELECT 
    uf, 
    br, 
    km, 
    sentido, 
    municipio, 
    area,
    latitude,
    longitude
FROM (
    SELECT DISTINCT 
        uf, 
        br, 
        km, 
        sentido_via AS sentido, 
        municipio, 
        uso_solo AS area,
        latitude,
        longitude
    FROM "silver"."stg"
);

MERGE INTO "silver"."dim_local" AS target 
USING temp_dim_local AS source 
    ON target.uf = source.uf 
    AND target.br = source.br 
    AND target.km = source.km 
    AND target.sentido = source.sentido 
    AND target.municipio = source.municipio 
    AND target.area = source.area
    AND target.latitude = source.latitude
    AND target.longitude = source.longitude

WHEN NOT MATCHED THEN 
INSERT (
    id, 
    uf, 
    br, 
    km, 
    sentido, 
    municipio, 
    area,
    latitude,
    longitude
) 
VALUES (
    nextval('seq_dim_local'), 
    source.uf, 
    source.br, 
    source.km, 
    source.sentido, 
    source.municipio, 
    source.area,
    source.latitude,
    source.longitude
);

DROP TABLE IF EXISTS temp_dim_local;