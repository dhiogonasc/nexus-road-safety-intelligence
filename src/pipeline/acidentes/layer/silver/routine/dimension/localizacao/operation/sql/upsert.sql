SELECT setval(
    'seq_dim_localizacao', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."dim_localizacao"), 0), 1)
);

CREATE TEMP TABLE temp_dim_localizacao AS 
SELECT 
    nextval('seq_dim_localizacao') AS id, 
    uf, br, km, uop, 
    municipio, 
    regional, 
    delegacia
FROM (
    SELECT DISTINCT 
        uf, br, km, uop, 
        municipio, 
        regional, 
        delegacia
    FROM "silver"."ultima_carga"
);

MERGE INTO "silver"."dim_localizacao" AS target 
USING temp_dim_localizacao AS source 
    ON target.uf = source.uf 
    AND target.br = source.br 
    AND target.km = source.km 
    AND target.uop = source.uop 
    AND target.municipio = source.municipio 
    AND target.regional = source.regional 
    AND target.delegacia = source.delegacia

WHEN NOT MATCHED THEN 
INSERT (
    id, 
    uf, br, km, uop, 
    municipio, 
    regional, 
    delegacia
) 
VALUES (
    source.id, 
    source.uf, 
    source.br, 
    source.km, 
    source.uop, 
    source.municipio, 
    source.regional, 
    source.delegacia
    );

DROP TABLE IF EXISTS temp_dim_localizacao;