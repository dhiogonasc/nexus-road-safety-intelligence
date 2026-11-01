MERGE INTO "{catalog_name}"."analytics"."agg_letalidade_clima_tempo" AS target
USING (
    SELECT * 
    FROM read_parquet('{storage_path}/**/*.parquet')
) AS source
ON target.id = source.id

WHEN MATCHED THEN 
    UPDATE SET 
        total_ocorrencias = source.total_ocorrencias,
        pct_mortalidade = source.pct_mortalidade

WHEN NOT MATCHED THEN 
    INSERT (
        id,
        uf,
        area,
        condicao_metereologica,
        mes,
        fase_dia,
        classificacao_acidente,
        total_ocorrencias,
        pct_mortalidade
    )
    VALUES (
        source.id,
        source.uf,
        source.area,
        source.condicao_metereologica,
        source.mes,
        source.fase_dia,
        source.classificacao_acidente,
        source.total_ocorrencias,
        source.pct_mortalidade
    );