MERGE INTO "{catalog_name}"."core"."ft_ocorrencia" AS target
USING (
    SELECT * 
    FROM read_parquet('{storage_path}/**/*.parquet')
) AS source
ON target.id = source.id

WHEN MATCHED THEN 
    UPDATE SET 
        pessoas = source.pessoas,
        mortos = source.mortos,
        feridos_leves = source.feridos_leves,
        feridos_graves = source.feridos_graves,
        feridos = source.feridos,
        ilesos = source.ilesos,
        ignorados = source.ignorados,
        veiculos = source.veiculos

WHEN NOT MATCHED THEN 
    INSERT (
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
        veiculos
    )
    VALUES (
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
        source.veiculos
    );