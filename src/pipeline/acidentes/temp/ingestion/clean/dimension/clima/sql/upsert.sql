SELECT setval(
    'seq_dim_clima', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."dim_clima"), 0), 1)
);

CREATE TEMP TABLE temp_dim_clima AS 
SELECT condicao
FROM (
    SELECT DISTINCT condicao_metereologica AS condicao
    FROM "silver"."stg_ocorrencia"
);

MERGE INTO "silver"."dim_clima" AS target 
USING temp_dim_clima AS source 
    ON target.condicao = source.condicao

WHEN NOT MATCHED THEN 
INSERT (
    id, 
    condicao
) 
VALUES (
    nextval('seq_dim_clima'),
    source.condicao
);

DROP TABLE IF EXISTS temp_dim_clima;