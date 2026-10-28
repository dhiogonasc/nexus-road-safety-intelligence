INSERT INTO "gold"."agg_letalidade_clima_tempo"(
    id,

    uf,
    municipio,

    condicao_metereologica,
    mes,
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
    source.municipio,

    source.condicao_metereologica,
    source.mes,
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
    FROM "gold"."agg_letalidade_clima_tempo" AS target 
    WHERE target.id = source.id
);