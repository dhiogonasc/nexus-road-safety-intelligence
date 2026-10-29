INSERT INTO "gold"."agg_dispersao_geo_temporal"(
    id,

    uf,
    area,
    municipio,

    ano,
    mes,
    dia_semana,

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
    source.area,
    source.municipio,

    source.ano,
    source.mes,
    source.dia_semana,

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
    FROM "gold"."agg_dispersao_geo_temporal" AS target 
    WHERE target.id = source.id
);