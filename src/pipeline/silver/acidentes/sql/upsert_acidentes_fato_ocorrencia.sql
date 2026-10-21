CREATE TEMP TABLE temp_fato_ocorrencias AS 
SELECT 
    COALESCE((SELECT MAX(id) FROM "silver"."fato_ocorrencia"), 0) + ROW_NUMBER() OVER () AS id,
    source_data.id_carga,
    source_data.id_ocorrencia,
    COALESCE(t.id, 0) AS sk_tempo,
    COALESCE(l.id, 0) AS sk_localizacao,
    COALESCE(coord.id, 0) AS sk_coordenada,
    COALESCE(causa.id, 0) AS sk_causa,
    COALESCE(tipo.id, 0) AS sk_tipo,
    COALESCE(classif.id, 0) AS sk_classificacao,
    COALESCE(p.id, 0) AS sk_pista,
    COALESCE(cond.id, 0) AS sk_condicao_metereologica,
    source_data.pessoas,
    source_data.mortos,
    source_data.feridos_leves,
    source_data.feridos_graves,
    source_data.feridos,
    source_data.ilesos,
    source_data.ignorados,
    source_data.veiculos
FROM (
    SELECT 
        max(id_carga) AS id_carga, 
        COALESCE(id :: VARCHAR, 'nao_informado') AS id_ocorrencia,
        (TRY_CAST(data_inversa AS DATE) + TRY_CAST(horario AS TIME)) AS data_hora,
        TRIM(COALESCE(uf :: VARCHAR, 'nao_informado')) AS uf,
        TRIM(COALESCE(br :: VARCHAR, 'nao_informado')) AS br,
        TRY_CAST(REPLACE(km :: VARCHAR, ',', '.') AS DOUBLE) AS km,
        TRIM(COALESCE(municipio :: VARCHAR, 'nao_informado')) AS municipio,
        TRIM(COALESCE(regional :: VARCHAR, 'nao_informado')) AS regional,
        TRIM(COALESCE(delegacia :: VARCHAR, 'nao_informado')) AS delegacia,
        TRIM(COALESCE(uop :: VARCHAR, 'nao_informado')) AS uop,
        TRY_CAST(REPLACE(latitude :: VARCHAR, ',', '.') AS DOUBLE) AS latitude,
        TRY_CAST(REPLACE(longitude :: VARCHAR, ',', '.') AS DOUBLE) AS longitude,
        COALESCE(causa_acidente :: VARCHAR, 'nao_informado') AS causa_acidente,
        COALESCE(tipo_acidente :: VARCHAR, 'nao_informado') AS tipo_acidente,
        COALESCE(classificacao_acidente :: VARCHAR, 'nao_informado') AS classificacao_acidente,
        COALESCE(condicao_metereologica :: VARCHAR, 'nao_informado') AS condicao_metereologica,
        COALESCE(sentido_via :: VARCHAR, 'nao_informado') AS sentido_via,
        COALESCE(tracado_via :: VARCHAR, 'nao_informado') AS tracado_via,
        COALESCE(tipo_pista :: VARCHAR, 'nao_informado') AS tipo_pista,
        COALESCE(uso_solo :: VARCHAR, 'nao_informado') AS uso_solo,
        COALESCE(pessoas, 0) AS pessoas,
        COALESCE(mortos, 0) AS mortos,
        COALESCE(feridos_leves, 0) AS feridos_leves,
        COALESCE(feridos_graves, 0) AS feridos_graves,
        COALESCE(feridos, 0) AS feridos,
        COALESCE(ilesos, 0) AS ilesos,
        COALESCE(ignorados, 0) AS ignorados,
        COALESCE(veiculos, 0) AS veiculos
    FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet')
    GROUP BY 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28
) AS source_data
LEFT JOIN "silver"."dim_tempo" AS t 
    ON source_data.data_hora = t.data_hora
LEFT JOIN "silver"."dim_localizacao" AS l 
    ON source_data.uf = l.uf 
   AND source_data.br = l.br 
   AND source_data.km = l.km
   AND source_data.municipio = l.municipio 
   AND source_data.regional = l.regional 
   AND source_data.delegacia = l.delegacia 
   AND source_data.uop = l.uop
LEFT JOIN "silver"."dim_coordenada" AS coord 
    ON source_data.latitude = coord.latitude 
   AND source_data.longitude = coord.longitude
LEFT JOIN "silver"."dim_causa" AS causa 
    ON source_data.causa_acidente = causa.causa
LEFT JOIN "silver"."dim_tipo" AS tipo 
    ON source_data.tipo_acidente = tipo.tipo
LEFT JOIN "silver"."dim_classificacao" AS classif 
    ON source_data.classificacao_acidente = classif.classificacao
LEFT JOIN "silver"."dim_pista" AS p 
    ON source_data.sentido_via = p.sentido
   AND source_data.tracado_via = p.tracado
   AND source_data.tipo_pista = p.tipo
   AND source_data.uso_solo = p.uso_solo
LEFT JOIN "silver"."dim_condicao_metereologica" AS cond
    ON source_data.condicao_metereologica = cond.condicao;

MERGE INTO "silver"."fato_ocorrencia" AS target 
USING temp_fato_ocorrencias AS source 
ON target.id_ocorrencia = source.id_ocorrencia

WHEN MATCHED THEN 
UPDATE SET 
    id = source.id,
    id_carga = source.id_carga,
    sk_tempo = source.sk_tempo,
    sk_localizacao = source.sk_localizacao,
    sk_coordenada = source.sk_coordenada,
    sk_causa = source.sk_causa,
    sk_tipo = source.sk_tipo,
    sk_classificacao = source.sk_classificacao,
    sk_pista = source.sk_pista,
    sk_condicao_metereologica = source.sk_condicao_metereologica,
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
    id_carga,
    id_ocorrencia, 
    sk_tempo, 
    sk_localizacao, 
    sk_coordenada, 
    sk_causa, 
    sk_tipo, 
    sk_classificacao, 
    sk_pista, 
    sk_condicao_metereologica, 
    pessoas, 
    mortos, 
    feridos_leves, 
    feridos_graves, 
    feridos, 
    ilesos, 
    ignorados, 
    veiculos
) 
VALUES (
    source.id, 
    source.id_carga,
    source.id_ocorrencia, 
    source.sk_tempo, 
    source.sk_localizacao, 
    source.sk_coordenada, 
    source.sk_causa, 
    source.sk_tipo, 
    source.sk_classificacao, 
    source.sk_pista, 
    source.sk_condicao_metereologica, 
    source.pessoas, 
    source.mortos, 
    source.feridos_leves, 
    source.feridos_graves, 
    source.feridos, 
    source.ilesos, 
    source.ignorados, 
    source.veiculos
);

DROP TABLE IF EXISTS temp_fato_ocorrencias;