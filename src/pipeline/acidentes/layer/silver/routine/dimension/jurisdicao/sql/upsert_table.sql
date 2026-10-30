SELECT setval(
    'seq_dim_jurisdicao', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."dim_jurisdicao"), 0), 1)
);

CREATE TEMP TABLE temp_dim_jurisdicao AS 
SELECT 
    uop,
    regional,
    delegacia
FROM (
    SELECT DISTINCT 
        uop,
        regional,
        delegacia
    FROM "silver"."stg"
);

MERGE INTO "silver"."dim_jurisdicao" AS target 
USING temp_dim_jurisdicao AS source 
    ON target.uop = source.uop
    AND target.regional = source.regional
    AND target.delegacia = source.delegacia

WHEN NOT MATCHED THEN 
INSERT (
    id, 
    uop,
    regional,
    delegacia
) 
VALUES (
    nextval('seq_dim_jurisdicao'),
    source.uop,
    source.regional,
    source.delegacia
);

DROP TABLE IF EXISTS temp_dim_jurisdicao;