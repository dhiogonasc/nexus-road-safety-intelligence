CREATE SEQUENCE IF NOT EXISTS "seq_trechos_criticos" START 1;

CREATE TABLE IF NOT EXISTS "gold"."agg_trechos_criticos" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_trechos_criticos'),

    uf VARCHAR NOT NULL,
    br VARCHAR NOT NULL,
    km DOUBLE PRECISION NOT NULL,
    sentido VARCHAR NOT NULL,
    area VARCHAR NOT NULL,
    tracado_via VARCHAR NOT NULL,
    tipo_via VARCHAR NOT NULL,
    classificacao_acidente VARCHAR NOT NULL,

    total_ocorrencias BIGINT NOT NULL,
    pct_mortalidade DOUBLE PRECISION NOT NULL,

    CONSTRAINT "uq_agg_trechos_criticos" UNIQUE (
        uf, 
        br, 
        km, 
        sentido,
        area, 
        sentido_via,
        tracado_via,
        tipo_via,
        classificacao_acidente
    )
);
