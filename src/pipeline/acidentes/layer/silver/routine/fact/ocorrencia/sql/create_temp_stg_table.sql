CREATE TABLE IF NOT EXISTS "silver"."temp_ft_ocorrencia_{ano}_{uf}" AS 
SELECT 
    fato.id_ocorrencia,
    COALESCE(tempo.id, 0) AS sk_tempo,
    COALESCE(local.id, 0) AS sk_local,
    COALESCE(pista.id, 0) AS sk_pista,
    COALESCE(jurisdicao.id, 0) AS sk_jurisdicao,
    COALESCE(clima.id, 0) AS sk_clima,
    COALESCE(categoria.id, 0) AS sk_categoria,
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
    WHERE ano = '{ano}' AND uf = '{uf}'
) AS fato

LEFT JOIN "silver"."dim_tempo" AS tempo 
    ON fato.data_hora = tempo.data_hora
    AND fato.dia_semana = tempo.dia_semana
    AND fato.fase_dia = tempo.fase_dia

LEFT JOIN "silver"."dim_local" AS local 
    ON fato.uf = local.uf 
    AND fato.br = local.br 
    AND fato.km = local.km
    AND fato.sentido_via = local.sentido 
    AND fato.municipio = local.municipio 
    AND fato.uso_solo = local.area
    AND fato.latitude = local.latitude 
    AND fato.longitude = local.longitude

LEFT JOIN "silver"."dim_pista" AS pista 
    ON fato.tipo_pista = pista.tipo
    AND fato.tracado_via = pista.tracado

LEFT JOIN "silver"."dim_jurisdicao" AS jurisdicao 
    ON fato.uop = jurisdicao.uop 
    AND fato.regional = jurisdicao.regional 
    AND fato.delegacia = jurisdicao.delegacia

LEFT JOIN "silver"."dim_clima" AS clima
    ON fato.condicao_metereologica = clima.condicao

LEFT JOIN "silver"."dim_categoria" AS categoria 
    ON fato.classificacao_acidente = categoria.classificacao 
    AND fato.causa_acidente = categoria.causa 
    AND fato.tipo_acidente = categoria.tipo;