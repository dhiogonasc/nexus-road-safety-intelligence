MERGE INTO "{catalog_name}"."core"."dim_categoria" AS target
USING (
    SELECT * 
    FROM read_parquet('{storage_path}/**/*.parquet')
) AS source
ON target.id = source.id

WHEN NOT MATCHED THEN 
    INSERT (
        id,
        classificacao,
        causa,
        tipo
    )
    VALUES (
        source.id,
        source.classificacao,
        source.causa,
        source.tipo
    );