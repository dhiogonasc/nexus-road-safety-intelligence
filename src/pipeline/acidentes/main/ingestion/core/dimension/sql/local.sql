MERGE INTO "{catalog_name}"."core"."dim_local" AS target
USING (
    SELECT * 
    FROM read_parquet('{storage_path}/**/*.parquet')
) AS source
ON target.id = source.id

WHEN NOT MATCHED THEN 
    INSERT (
        id,
        uf, 
        br, 
        km, 
        sentido, 
        municipio, 
        area,
        latitude,
        longitude
    )
    VALUES (
        source.id,
        source.uf, 
        source.br, 
        source.km, 
        source.sentido, 
        source.municipio, 
        source.area,
        source.latitude,
        source.longitude
    );