INSERT INTO "gold"."agg_trechos_criticos"(
    id,
    uf,
    br,
    km,
    sentido,
    area,
    tracado_via,
    tipo_via,
    classificacao_acidente,
    total_ocorrencias,
    pct_mortalidade
)
SELECT 
    source.id,
    source.uf,
    source.br,
    source.km,
    source.sentido,
    source.area,
    source.tracado_via,
    source.tipo_via,
    source.classificacao_acidente,
    source.total_ocorrencias,
    source.pct_mortalidade
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "gold"."agg_trechos_criticos" AS target 
    WHERE target.id = source.id
);