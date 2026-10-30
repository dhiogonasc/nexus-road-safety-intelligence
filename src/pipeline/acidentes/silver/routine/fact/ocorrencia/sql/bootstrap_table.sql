INSERT INTO "silver"."ft_ocorrencia" (
    id,
    id_ocorrencia,
    sk_tempo,
    sk_local,
    sk_pista,
    sk_jurisdicao,
    sk_clima,
    sk_categoria,
    pessoas,
    mortos,
    feridos_leves,
    feridos_graves,
    feridos,
    ilesos,
    ignorados,
    veiculos,
    ano,
    uf,
)
SELECT 
    source.id,
    source.id_ocorrencia,
    source.sk_tempo,
    source.sk_local,
    source.sk_pista,
    source.sk_jurisdicao,
    source.sk_clima,
    source.sk_categoria,
    source.pessoas,
    source.mortos,
    source.feridos_leves,
    source.feridos_graves,
    source.feridos,
    source.ilesos,
    source.ignorados,
    source.veiculos,
    source.ano,
    source.uf
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "silver"."ft_ocorrencia" AS target 
    WHERE target.id = source.id
);