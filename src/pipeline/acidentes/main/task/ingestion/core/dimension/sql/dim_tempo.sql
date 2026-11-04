MERGE INTO "{catalog_name}"."core"."dim_tempo" AS target
USING (
    SELECT * 
    FROM read_parquet('{storage_path}/**/*.parquet')
) AS source
ON target.id = source.id

WHEN NOT MATCHED THEN 
    INSERT (
        id,
        ano,
        mes,
        semana,
        dia_semana,
        fase_dia,
        mes_str,
        dia_semana_str,
        fase_dia_str
    )
    VALUES (
        source.id,
        source.ano,
        source.mes,
        source.semana,
        source.dia_semana,
        source.fase_dia,
        source.mes_str,
        source.dia_semana_str,
        source.fase_dia_str
    );