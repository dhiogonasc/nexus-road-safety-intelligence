MERGE INTO "{catalog_name}"."analytics"."agg_letalidade_pista_tempo" AS target
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
        br, 
        area,
        tracado_via,
        tipo_via,
        mes, 
        dia_semana, 
        fase_dia,
        classificacao_acidente,
        total_ocorrencias,
        pct_mortalidade
    )
    VALUES (
        source.id,
        source.uf,
        source.br,
        source.area,
        source.tracado_via,
        source.tipo_via,
        source.mes,
        source.dia_semana,
        source.fase_dia,
        source.classificacao_acidente,
        source.total_ocorrencias,
        source.pct_mortalidade
    );