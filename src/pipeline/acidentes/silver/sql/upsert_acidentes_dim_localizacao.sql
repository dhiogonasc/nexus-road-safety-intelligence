SELECT setval(
    'seq_dim_localizacao', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."dim_localizacao"), 0), 1)
);

CREATE TEMP TABLE temp_dim_localizacao AS 
SELECT 
    nextval('seq_dim_localizacao') AS id,
    source_data.uf,
    source_data.br,
    source_data.municipio,
    source_data.regional,
    source_data.delegacia,
    source_data.uop,
    source_data.km
FROM (
    SELECT uf, br, km, municipio, regional, delegacia, uop
    FROM "silver"."last_charged"
) AS source_data;

MERGE INTO "silver"."dim_localizacao" AS target 
USING temp_dim_localizacao AS source 
    ON target.uf = source.uf
    AND target.br = source.br
    AND target.municipio = source.municipio
    AND target.regional = source.regional
    AND target.delegacia = source.delegacia
    AND target.uop = source.uop
    AND target.km = source.km

WHEN NOT MATCHED THEN 
INSERT (
    id, 
    uf, 
    br, 
    municipio, 
    regional, 
    delegacia, 
    uop, 
    km
) 
VALUES (
    source.id,
    source.uf, 
    source.br, 
    source.municipio, 
    source.regional, 
    source.delegacia, 
    source.uop,
    source.km
);

DROP TABLE IF EXISTS temp_dim_localizacao;