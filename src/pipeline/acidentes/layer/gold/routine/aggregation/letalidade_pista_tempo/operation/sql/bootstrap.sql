INSERT INTO "gold"."agg_letalidade_pista_tempo"(
    id,

    uf,
    br,
    municipio,

    sentido_via,
    tracado_via,
    tipo_via,
    solo_via,

    mes,
    dia_semana,
    fase_dia,

    causa_acidente,
    classificacao_acidente,
    tipo_acidente,

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

    source.uf,
    source.br,
    source.municipio,

    source.sentido_via,
    source.tracado_via,
    source.tipo_via,
    source.solo_via,
    
    source.mes,
    source.dia_semana,
    source.fase_dia,

    source.causa_acidente,
    source.classificacao_acidente,
    source.tipo_acidente,

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
    FROM "gold"."agg_letalidade_pista_tempo" AS target 
    WHERE target.id = source.id
);