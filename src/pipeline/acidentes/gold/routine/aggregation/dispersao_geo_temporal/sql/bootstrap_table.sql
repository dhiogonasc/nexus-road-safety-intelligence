INSERT INTO "gold"."agg_dispersao_geo_temporal"(
    id,
    uf,
    area,
    municipio,
    ano,
    mes,
    dia_semana,
    total_ocorrencias,
    pct_mortalidade
)
SELECT 
    source.id,
    source.uf,
    source.area,
    source.municipio,
    source.ano,
    source.mes,
    source.dia_semana,
    source.total_ocorrencias,
    source.pct_mortalidade
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "gold"."agg_dispersao_geo_temporal" AS target 
    WHERE target.id = source.id
);