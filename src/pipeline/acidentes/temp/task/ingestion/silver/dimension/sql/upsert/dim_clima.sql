SELECT setval(
    'seq_dim_clima', 
    COALESCE((SELECT MAX(id) FROM "silver"."dim_clima"), 1)
);

MERGE INTO "silver"."dim_clima" AS target 
USING (
    SELECT DISTINCT condicao_metereologica AS condicao
    FROM "silver"."stg_ocorrencias"
) AS source 
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
