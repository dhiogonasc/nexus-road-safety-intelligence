INSERT INTO "silver"."ft_ocorrencia" (
    id,

    id_ocorrencia,
    sk_tempo,
    sk_localizacao,
    sk_coordenada,
    sk_causa,
    sk_tipo,
    sk_classificacao,
    sk_pista,
    sk_condicao_metereologica,

    pessoas,
    mortos,
    feridos_leves,
    feridos_graves,
    feridos,
    ilesos,
    ignorados,
    veiculos
)
SELECT 
    source.id,

    source.id_ocorrencia,
    source.sk_tempo,
    source.sk_localizacao,
    source.sk_coordenada,
    source.sk_causa,
    source.sk_tipo,
    source.sk_classificacao,
    source.sk_pista,
    source.sk_condicao_metereologica,
    
    source.pessoas,
    source.mortos,
    source.feridos_leves,
    source.feridos_graves,
    source.feridos,
    source.ilesos,
    source.ignorados,
    source.veiculos
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "silver"."ft_ocorrencia" AS target 
    WHERE target.id = source.id
);