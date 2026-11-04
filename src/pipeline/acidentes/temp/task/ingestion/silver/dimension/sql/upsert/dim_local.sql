SELECT setval(
    'seq_dim_local', 
    COALESCE((SELECT MAX(id) FROM "silver"."dim_local"), 1)
);

MERGE INTO "silver"."dim_local" AS target 
USING (
    SELECT DISTINCT 
        uf, 
        br, 
        km, 
        sentido, 
        tipo_area,
        municipio 
    FROM "silver"."stg_ocorrencias"
) AS source 
    ON target.uf = source.uf 
    AND target.br = source.br 
    AND target.km = source.km 
    AND target.sentido = source.sentido 
    AND target.tipo_area = source.tipo_area
    AND target.municipio = source.municipio 

WHEN NOT MATCHED THEN 
INSERT (
    id,
    uf, 
    br, 
    km, 
    sentido, 
    tipo_area,
    municipio 
) 
VALUES (
    nextval('seq_dim_local'),
    source.uf, 
    source.br, 
    source.km, 
    source.sentido, 
    source.tipo_area,
    source.municipio
);
