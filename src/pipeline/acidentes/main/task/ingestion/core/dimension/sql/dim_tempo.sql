MERGE INTO "{catalog_name}"."core"."dim_tempo" AS target
USING (
    SELECT * 
    FROM read_parquet('{source_storage_path}/**/*.parquet')
) AS source
ON target.id = source.id

WHEN NOT MATCHED THEN 
    INSERT (
        id,
        ano,
        mes,
        semana,
        dia_semana,
        fase_dia
    )
    VALUES (
        source.id,
        source.ano,
        source.mes,
        source.semana,
        source.dia_semana,
        source.fase_dia
    );