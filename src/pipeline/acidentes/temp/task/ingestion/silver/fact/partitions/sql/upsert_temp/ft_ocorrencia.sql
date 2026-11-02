CREATE TABLE IF NOT EXISTS "silver"."temp_ft_ocorrencia_{partition_values}" AS 
SELECT 
    fato.id_ocorrencia,
    COALESCE(local.id, 0) AS sk_local,
    COALESCE(tempo.id, 0) AS sk_tempo,
    COALESCE(clima.id, 0) AS sk_clima,
    COALESCE(categoria.id, 0) AS sk_categoria,
    fato.pessoas,
    fato.mortos,
    fato.feridos_leves,
    fato.feridos_graves,
    fato.feridos,
    fato.ilesos,
    fato.ignorados,
    fato.veiculos,
    tempo.ano,
    local.uf
FROM (
    SELECT *
    FROM read_parquet('{staging_storage_path}/**/*.parquet', hive_partitioning = true)
    WHERE 1=1
    {filter_clause}
) AS fato

LEFT JOIN "silver"."dim_local" AS local 
    ON fato.uf = local.uf 
    AND fato.br = local.br 
    AND fato.km = local.km
    AND fato.sentido = local.sentido 
    AND fato.tipo_area = local.tipo_area
    AND fato.municipio = local.municipio 

LEFT JOIN "silver"."dim_tempo" AS tempo 
    ON fato.ano = tempo.ano
    AND fato.mes = tempo.mes
    AND fato.semana = tempo.semana
    AND fato.dia_semana = tempo.dia_semana
    AND fato.fase_dia = tempo.fase_dia

LEFT JOIN "silver"."dim_clima" AS clima
    ON fato.condicao_metereologica = clima.condicao

LEFT JOIN "silver"."dim_categoria" AS categoria 
    ON fato.tipo = categoria.tipo
    AND fato.causa = categoria.causa 
    AND fato.classificacao = categoria.classificacao;

MERGE INTO "silver"."temp_ft_ocorrencia" AS target 
USING "silver"."temp_ft_ocorrencia_{partition_values}" AS source 
    ON target.id_ocorrencia = source.id_ocorrencia
    AND target.sk_local = source.sk_local
    AND target.sk_tempo = source.sk_tempo
    AND target.sk_clima = source.sk_clima
    AND target.sk_categoria = source.sk_categoria


WHEN MATCHED THEN 
UPDATE SET 
    pessoas = source.pessoas,
    mortos = source.mortos,
    feridos_leves = source.feridos_leves,
    feridos_graves = source.feridos_graves,
    feridos = source.feridos,
    ilesos = source.ilesos,
    ignorados = source.ignorados,
    veiculos = source.veiculos

WHEN NOT MATCHED THEN 
INSERT (
    id_ocorrencia, 
    sk_local, 
    sk_tempo, 
    sk_clima, 
    sk_categoria, 
    pessoas, 
    mortos, 
    feridos_leves, 
    feridos_graves, 
    feridos, 
    ilesos, 
    ignorados, 
    veiculos,
    ano,
    uf
) 
VALUES (
    source.id_ocorrencia, 
    source.sk_local, 
    source.sk_tempo, 
    source.sk_clima, 
    source.sk_categoria,
    source.pessoas, 
    source.mortos, 
    source.feridos_leves, 
    source.feridos_graves, 
    source.feridos, 
    source.ilesos, 
    source.ignorados, 
    source.veiculos,
    source.ano,
    source.uf
);

DROP TABLE IF EXISTS "silver"."temp_ft_ocorrencia_{partition_values}";
