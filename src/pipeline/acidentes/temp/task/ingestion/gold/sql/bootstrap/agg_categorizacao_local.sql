INSERT INTO "gold"."agg_categorizacao_local" (
    id, 
    uf, 
    br, 
    km, 
    sentido,
    tipo_area, 
    municipio,
    tipo_acidente,
    causa_acidente,
    classificacao_acidente,
    total_mortos,
    total_envolvidos,
    total_ocorrencias,
    taxa_mortalidade_por_ocorrencia,
    taxa_mortalidade_por_envolvido
)
SELECT 
    source.id, 
    source.uf, 
    source.br, 
    source.km, 
    source.sentido,
    source.tipo_area, 
    source.municipio,
    source.tipo_acidente,
    source.causa_acidente,
    source.classificacao_acidente,
    source.total_mortos,
    source.total_envolvidos,
    source.total_ocorrencias,
    source.taxa_mortalidade_por_ocorrencia,
    source.taxa_mortalidade_por_envolvido
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "gold"."agg_categorizacao_local" AS target 
    WHERE target.id = source.id
);