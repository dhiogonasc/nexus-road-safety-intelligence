MERGE INTO "{catalog_name}"."core"."dim_tempo" AS target
USING (
    SELECT * 
    FROM read_parquet('{storage_path}/**/*.parquet')
) AS source
ON target.id = source.id

WHEN NOT MATCHED THEN 
    INSERT (
        id,
        data_hora,
        ano,
        mes,
        dia,
        hora,
        dia_semana,
        fase_dia
    )
    VALUES (
        source.id,
        source.data_hora,
        source.ano,
        source.mes,
        source.dia,
        source.hora,
        source.dia_semana,
        source.fase_dia
    );