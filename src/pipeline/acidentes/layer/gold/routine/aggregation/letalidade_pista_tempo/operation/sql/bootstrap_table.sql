INSERT INTO "gold"."agg_letalidade_pista_tempo"(
    id,
    uf,
    br,
    area,
    tracado_via,
    tipo_via,
    mes,
    dia_semana,
    fase_dia,
    classificacao_acidente,
    total_ocorrencias,
    pct_mortalidade
)
SELECT 
    source.id,
    source.uf,
    source.br,
    source.area,
    source.tracado_via,
    source.tipo_via,
    source.mes,
    source.dia_semana,
    source.fase_dia,
    source.classificacao_acidente,
    source.total_ocorrencias,
    source.pct_mortalidade
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "gold"."agg_letalidade_pista_tempo" AS target 
    WHERE target.id = source.id
);