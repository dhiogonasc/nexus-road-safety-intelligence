MERGE INTO "{catalog_name}"."core"."dim_categoria" AS target
USING (
    SELECT * 
    FROM read_parquet('{source_storage_path}/**/*.parquet')
) AS source
ON target.id = source.id

WHEN NOT MATCHED THEN 
    INSERT (
        id,
        tipo,
        causa,
        classificacao
    )
    VALUES (
        source.id,
        source.tipo,
        source.causa,
        source.classificacao
    );