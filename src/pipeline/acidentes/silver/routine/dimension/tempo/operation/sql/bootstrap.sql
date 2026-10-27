INSERT INTO "silver"."dim_tempo"(
    id,
    data_hora,
    ano, mes, dia, hora, 
    dia_semana, fase_dia
)
SELECT 
    source.id,
    source.data_hora,
    source.ano, 
    source.mes, 
    source.dia, 
    source.hora,
    source.dia_semana, 
    source.fase_dia
FROM read_parquet('{storage_path}/**/*.parquet') AS source
WHERE NOT EXISTS (
    SELECT 1 
    FROM "silver"."dim_tempo" AS target 
    WHERE target.id = source.id
);