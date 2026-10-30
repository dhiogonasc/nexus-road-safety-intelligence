INSERT INTO "gold"."agg_letalidade_clima_tempo"(
    id,
    uf,
    area,
    condicao_metereologica,
    mes,
    fase_dia,
    classificacao_acidente,
    total_ocorrencias,
    pct_mortalidade
)
SELECT 
    source.id,
    source.uf,
    source.area,
    source.condicao_metereologica,
    source.mes,
    source.fase_dia,
    source.classificacao_acidente,
    source.total_ocorrencias,
    source.pct_mortalidade
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "gold"."agg_letalidade_clima_tempo" AS target 
    WHERE target.id = source.id
);