INSERT INTO "gold"."agg_letalidade_pista_clima"(
    id,
    uf,
    br,
    area,
    tracado_via,
    tipo_via,
    condicao_metereologica,
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
    source.condicao_metereologica,
    source.classificacao_acidente,
    source.total_ocorrencias,
    source.pct_mortalidade
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "gold"."agg_letalidade_pista_clima" AS target 
    WHERE target.id = source.id
);