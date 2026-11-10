CREATE TABLE IF NOT EXISTS "silver"."fct_ocorrencia" (
    id VARCHAR NOT NULL PRIMARY KEY,

    id_ocorrencia BIGINT NOT NULL,
    sk_local INTEGER NOT NULL,
    sk_tempo INTEGER NOT NULL,
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

    -- base de particao
    ano INTEGER NOT NULL,
    uf VARCHAR NOT NULL,

    CONSTRAINT "uq_fct_ocorrencia" UNIQUE (
        id_ocorrencia,
        sk_local,
        sk_tempo,
        sk_clima,
        sk_categoria
    )
);