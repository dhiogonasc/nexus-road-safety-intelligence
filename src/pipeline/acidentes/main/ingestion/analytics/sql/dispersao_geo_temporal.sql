MERGE INTO "{catalog_name}"."analytics"."agg_dispersao_geo_temporal" AS target
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
        municipio,
        ano,
        mes,
        dia_semana,
        total_ocorrencias,
        pct_mortalidade
    )
    VALUES (
        source.id,
        source.uf,
        source.area,
        source.municipio,
        source.ano,
        source.mes,
        source.dia_semana,
        source.total_ocorrencias,
        source.pct_mortalidade
    );