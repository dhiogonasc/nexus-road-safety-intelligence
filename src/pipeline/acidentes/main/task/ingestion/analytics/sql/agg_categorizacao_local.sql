MERGE INTO "{catalog_name}"."analytics"."agg_categorizacao_local" AS target
USING (
    SELECT * 
    FROM read_parquet('{source_storage_path}/**/*.parquet')
) AS source
ON target.id = source.id

WHEN MATCHED THEN 
    UPDATE SET 
        mortos = source.mortos,
        total_ocorrencias = source.total_ocorrencias,
        pct_mortalidade = source.pct_mortalidade

WHEN NOT MATCHED THEN 
    INSERT (
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
        mortos,
        total_ocorrencias,
        pct_mortalidade
    )
    VALUES (
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
        source.mortos,
        source.total_ocorrencias,
        source.pct_mortalidade
    );