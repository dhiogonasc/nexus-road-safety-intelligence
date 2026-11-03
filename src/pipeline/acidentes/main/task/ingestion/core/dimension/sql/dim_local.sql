MERGE INTO "{catalog_name}"."core"."dim_local" AS target
USING (
    SELECT * 
    FROM read_parquet('{source_storage_path}/**/*.parquet')
) AS source
ON target.id = source.id

WHEN NOT MATCHED THEN 
    INSERT (
        id,
        uf, 
        br, 
        km, 
        sentido, 
        tipo_area,
        municipio
    )
    VALUES (
        source.id,
        source.uf, 
        source.br, 
        source.km, 
        source.sentido, 
        source.tipo_area,
        source.municipio
    );