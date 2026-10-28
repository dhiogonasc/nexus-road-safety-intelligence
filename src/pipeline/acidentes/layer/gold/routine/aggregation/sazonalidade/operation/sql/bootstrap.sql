INSERT INTO "gold"."condicoes_via"(
    id,
    
    ano,
    mes,
    dia,
    dia_semana,
    fase_dia,


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
SELECT 
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
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "gold"."condicoes_via" AS target 
    WHERE target.id = source.id
);