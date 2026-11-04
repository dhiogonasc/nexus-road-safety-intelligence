MERGE INTO "{catalog_name}"."analytics"."agg_categorizacao_local" AS target
USING (
    SELECT * 
    FROM read_parquet('{storage_path}/**/*.parquet')
) AS source
ON target.id = source.id

WHEN MATCHED THEN 
    UPDATE SET 
        total_mortos = source.total_mortos,
        total_envolvidos = source.total_envolvidos,
        total_ocorrencias = source.total_ocorrencias,
        taxa_mortalidade_por_envolvido = source.taxa_mortalidade_por_envolvido,
        taxa_mortalidade_por_ocorrencia = source.taxa_mortalidade_por_ocorrencia

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
        total_mortos,
        total_envolvidos,
        total_ocorrencias,
        taxa_mortalidade_por_envolvido,
        taxa_mortalidade_por_ocorrencia
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
        source.total_mortos,
        source.total_envolvidos,
        source.total_ocorrencias,
        source.taxa_mortalidade_por_envolvido,
        source.taxa_mortalidade_por_ocorrencia
    );