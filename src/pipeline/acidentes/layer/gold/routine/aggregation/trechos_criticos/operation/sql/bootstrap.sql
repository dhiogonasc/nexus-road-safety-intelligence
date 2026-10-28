INSERT INTO "gold"."agg_trechos_criticos"(
    id,

    uf,
    br,
    km,
    uop,
    regional,
    municipio,
    delegacia,

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
SELECT 
    source.id,

    source.uf,
    source.br,
    source.km,
    source.uop,
    source.regional,
    source.municipio,
    source.delegacia,

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
    FROM "gold"."agg_trechos_criticos" AS target 
    WHERE target.id = source.id
);