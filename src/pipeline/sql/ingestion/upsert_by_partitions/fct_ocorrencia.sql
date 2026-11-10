MERGE INTO "silver"."fct_ocorrencia" AS target 
USING (
    SELECT 
        md5(
            COALESCE(CAST(fato.id_ocorrencia AS VARCHAR), '') || '-' ||
            COALESCE(CAST(local.id AS VARCHAR), '0') || '-' ||
            COALESCE(CAST(tempo.id AS VARCHAR), '0') || '-' ||
            COALESCE(CAST(clima.id AS VARCHAR), '0') || '-' ||
            COALESCE(CAST(categoria.id AS VARCHAR), '0')
        ) AS id,
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
        fato.ano,
        fato.uf
    FROM (
        SELECT *
        FROM read_parquet(
            '{stg_ocorrencias_storage_path}/**/*.parquet', 
            hive_partitioning = true
        )
        WHERE 1=1
        {filter_clause}
    ) AS fato

    JOIN (
        SELECT *
        FROM read_parquet('{dim_local_storage_path}/**/*.parquet')
    ) AS local 
        ON fato.uf = local.uf 
        AND fato.br = local.br 
        AND fato.km = local.km
        AND fato.sentido = local.sentido 
        AND fato.tipo_area = local.tipo_area
        AND fato.municipio = local.municipio 

    JOIN (
        SELECT *
        FROM read_parquet('{dim_tempo_storage_path}/**/*.parquet')
    ) AS tempo 
        ON fato.ano = tempo.ano
        AND fato.mes = tempo.mes
        AND fato.semana = tempo.semana
        AND fato.dia_semana = tempo.dia_semana
        AND fato.fase_dia = tempo.fase_dia

    JOIN (
        SELECT *
        FROM read_parquet('{dim_clima_storage_path}/**/*.parquet')
    ) AS clima
        ON fato.condicao_metereologica = clima.condicao

    JOIN (
        SELECT *
        FROM read_parquet('{dim_categoria_storage_path}/**/*.parquet')
    ) AS categoria 
        ON fato.tipo = categoria.tipo
        AND fato.causa = categoria.causa 
        AND fato.classificacao = categoria.classificacao
) AS source 
ON target.id = source.id

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
    id, 
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
    source.id,
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