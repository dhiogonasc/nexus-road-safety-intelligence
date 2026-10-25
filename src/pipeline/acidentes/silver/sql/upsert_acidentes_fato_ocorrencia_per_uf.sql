SELECT setval(
    'seq_fato_ocorrencia', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."fato_ocorrencia"), 0), 1)
);

CREATE TEMP TABLE temp_fato_ocorrencias AS 
SELECT 
    nextval('seq_fato_ocorrencia') AS id,
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
    SELECT *
    FROM "silver"."last_charged"
    WHERE uf = '{uf}'
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
    AND target.sk_tempo = source.sk_tempo
    AND target.sk_localizacao = source.sk_localizacao
    AND target.sk_coordenada = source.sk_coordenada
    AND target.sk_causa = source.sk_causa
    AND target.sk_tipo = source.sk_tipo
    AND target.sk_classificacao = source.sk_classificacao
    AND target.sk_pista = source.sk_pista
    AND target.sk_condicao_metereologica = source.sk_condicao_metereologica

WHEN MATCHED THEN 
UPDATE SET 
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