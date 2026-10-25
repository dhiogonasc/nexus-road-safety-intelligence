SELECT setval(
    'seq_dim_condicao_metereologica', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."dim_condicao_metereologica"), 0), 1)
);

CREATE TEMP TABLE temp_dim_condicao_metereologica AS 
SELECT 
    nextval('seq_dim_condicao_metereologica') AS id,
    source_data.condicao
FROM (
    SELECT condicao_metereologica AS condicao
    FROM "silver"."last_charged" 
) AS source_data;

MERGE INTO "silver"."dim_condicao_metereologica" AS target 
USING temp_dim_condicao_metereologica AS source 
ON target.condicao = source.condicao

WHEN NOT MATCHED THEN 
INSERT (id, condicao) 
VALUES (source.id, source.condicao);

DROP TABLE IF EXISTS temp_dim_condicao_metereologica;