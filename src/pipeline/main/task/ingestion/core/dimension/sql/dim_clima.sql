MERGE INTO "{catalog_name}"."core"."dim_clima" AS target
USING (
    SELECT * 
    FROM read_parquet('{storage_path}/**/*.parquet')
) AS source
ON target.id = source.id

WHEN NOT MATCHED THEN 
    INSERT (
        id,
        condicao
    )
    VALUES (
        source.id,
        source.condicao
    );