CREATE TEMP TABLE temp_agg_condicoes_via AS SELECT *
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/gold/agg_condicoes_via/agg_condicoes_via.parquet') ;

MERGE INTO "{catalog}"."analytics"."agg_condicoes_via" AS target 
USING temp_agg_condicoes_via AS source 
    ON target.id = source.id 

WHEN MATCHED THEN
UPDATE SET
    total_ocorrencias = source.total_ocorrencias,
    total_pessoas = source.total_pessoas,
    total_veiculos = source.total_veiculos,
    total_mortos = source.total_mortos,
    total_feridos = source.total_feridos,
    total_feridos_graves = source.total_feridos_graves,
    total_feridos_leves = source.total_feridos_leves,
    total_ilesos = source.total_ilesos,
    pct_mortalidade = source.pct_mortalidade

WHEN NOT MATCHED THEN 
INSERT (
    id,
    ano,
    mes,
    dia,
    dia_semana,
    fase_dia,
    condicao_metereologica,
    sentido_via,
    tracado_via,
    tipo_via,
    solo_via,
    total_ocorrencias,
    total_pessoas,
    total_veiculos,
    total_mortos,
    total_feridos,
    total_feridos_graves,
    total_feridos_leves,
    total_ilesos,
    pct_mortalidade
) 
VALUES (
    source.id,
    source.ano,
    source.mes,
    source.dia,
    source.dia_semana,
    source.fase_dia,
    source.condicao_metereologica,
    source.sentido_via,
    source.tracado_via,
    source.tipo_via,
    source.solo_via,
    source.total_ocorrencias,
    source.total_pessoas,
    source.total_veiculos,
    source.total_mortos,
    source.total_feridos,
    source.total_feridos_graves,
    source.total_feridos_leves,
    source.total_ilesos,
    source.pct_mortalidade
);

DROP TABLE IF EXISTS temp_agg_condicoes_via;