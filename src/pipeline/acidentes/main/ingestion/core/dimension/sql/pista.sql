MERGE INTO "{catalog_name}"."core"."dim_pista" AS target
USING (
    SELECT * 
    FROM read_parquet('{storage_path}/**/*.parquet')
) AS source
ON target.id = source.id

WHEN NOT MATCHED THEN 
    INSERT (
        id,
        tracado, 
        tipo
    )
    VALUES (
        source.id,
        source.tracado, 
        source.tipo
    );