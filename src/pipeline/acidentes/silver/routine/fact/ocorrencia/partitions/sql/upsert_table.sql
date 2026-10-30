SELECT setval(
    'seq_ft_ocorrencia', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "silver"."ft_ocorrencia"), 0), 1)
);

MERGE INTO "silver"."ft_ocorrencia" AS target 
USING "silver"."temp_ft_ocorrencia" AS source 
    ON target.id_ocorrencia = source.id_ocorrencia
    AND target.sk_tempo = source.sk_tempo
    AND target.sk_local = source.sk_local
    AND target.sk_pista = source.sk_pista
    AND target.sk_jurisdicao = source.sk_jurisdicao
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
    id, 
    id_ocorrencia, 
    sk_tempo, 
    sk_local, 
    sk_pista, 
    sk_jurisdicao, 
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
    nextval('seq_ft_ocorrencia'),
    source.id_ocorrencia, 
    source.sk_tempo, 
    source.sk_local, 
    source.sk_pista, 
    source.sk_jurisdicao, 
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

DROP TABLE IF EXISTS "silver"."temp_ft_ocorrencia";