SELECT setval(
    'seq_ft_ocorrencia', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."ft_ocorrencia"), 0), 1)
);

CREATE TEMP TABLE temp_ft_ocorrencias AS 
SELECT 
    nextval('seq_ft_ocorrencia') AS id,
    fato.id_ocorrencia,
    COALESCE(tempo.id, 0) AS sk_tempo,
    COALESCE(localizacao.id, 0) AS sk_localizacao,
    COALESCE(coordenada.id, 0) AS sk_coordenada,
    COALESCE(causa.id, 0) AS sk_causa,
    COALESCE(tipo.id, 0) AS sk_tipo,
    COALESCE(classificacao.id, 0) AS sk_classificacao,
    COALESCE(pista.id, 0) AS sk_pista,
    COALESCE(condicao_metereologica.id, 0) AS sk_condicao_metereologica,
    fato.pessoas,
    fato.mortos,
    fato.feridos_leves,
    fato.feridos_graves,
    fato.feridos,
    fato.ilesos,
    fato.ignorados,
    fato.veiculos
FROM (
    SELECT *
    FROM "silver"."stg"
    WHERE uf = '{uf}'
) AS fato

LEFT JOIN "silver"."dim_tempo" AS tempo 
    ON fato.data_hora = tempo.data_hora

LEFT JOIN "silver"."dim_localizacao" AS localizacao 
    ON fato.uf = localizacao.uf 
    AND fato.br = localizacao.br 
    AND fato.km = localizacao.km
    AND fato.municipio = localizacao.municipio 
    AND fato.regional = localizacao.regional 
    AND fato.delegacia = localizacao.delegacia 
    AND fato.uop = localizacao.uop

LEFT JOIN "silver"."dim_coordenada" AS coordenada 
    ON fato.latitude = coordenada.latitude 
    AND fato.longitude = coordenada.longitude

LEFT JOIN "silver"."dim_causa" AS causa 
    ON fato.causa_acidente = causa.causa

LEFT JOIN "silver"."dim_tipo" AS tipo 
    ON fato.tipo_acidente = tipo.tipo

LEFT JOIN "silver"."dim_classificacao" AS classificacao 
    ON fato.classificacao_acidente = classificacao.classificacao

LEFT JOIN "silver"."dim_pista" AS pista 
    ON fato.sentido_via = pista.sentido
    AND fato.tracado_via = pista.tracado
    AND fato.tipo_pista = pista.tipo
    AND fato.uso_solo = pista.solo

LEFT JOIN "silver"."dim_condicao_metereologica" AS condicao_metereologica
    ON fato.condicao_metereologica = condicao_metereologica.condicao;

MERGE INTO "silver"."ft_ocorrencia" AS target 
USING temp_ft_ocorrencias AS source 
    ON target.id_ocorrencia = source.id_ocorrencia
    AND target.sk_tempo = source.sk_tempo
    AND target.sk_localizacao = source.sk_localizacao
    AND target.sk_coordenada = source.sk_coordenada
    AND target.sk_pista = source.sk_pista
    AND target.sk_causa = source.sk_causa
    AND target.sk_tipo = source.sk_tipo
    AND target.sk_classificacao = source.sk_classificacao

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

DROP TABLE IF EXISTS temp_ft_ocorrencias;