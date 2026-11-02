MERGE INTO "{catalog_name}"."core"."dim_jurisdicao" AS target
USING (
    SELECT * 
    FROM read_parquet('{storage_path}/**/*.parquet')
) AS source
ON target.id = source.id

WHEN NOT MATCHED THEN 
    INSERT (
        id,
        uop,
        regional,
        delegacia

    )
    VALUES (
        source.id,
        source.uop,
        source.regional,
        source.delegacia
    );