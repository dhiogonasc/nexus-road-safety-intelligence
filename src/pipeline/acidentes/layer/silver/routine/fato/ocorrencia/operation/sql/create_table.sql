CREATE SEQUENCE IF NOT EXISTS "seq_ft_ocorrencia" START 1 INCREMENT 1;

CREATE TABLE IF NOT EXISTS "silver"."ft_ocorrencia" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_ft_ocorrencia'),

    id_ocorrencia BIGINT NOT NULL,
    sk_tempo INTEGER NOT NULL,
    sk_local INTEGER NOT NULL,
    sk_pista INTEGER NOT NULL,
    sk_jurisdicao INTEGER NOT NULL,
    sk_clima INTEGER NOT NULL,
    sk_categoria INTEGER NOT NULL,
    
    pessoas INTEGER NOT NULL,
    mortos INTEGER NOT NULL,
    feridos_leves INTEGER NOT NULL,
    feridos_graves INTEGER NOT NULL,
    feridos INTEGER NOT NULL,
    ilesos INTEGER NOT NULL,
    ignorados INTEGER NOT NULL,
    veiculos INTEGER NOT NULL,

    CONSTRAINT "uq_ft_ocorrencia" UNIQUE (
        id_ocorrencia,
        sk_tempo,
        sk_local,
        sk_pista,
        sk_jurisdicao,
        sk_clima,
        sk_categoria
    )
);