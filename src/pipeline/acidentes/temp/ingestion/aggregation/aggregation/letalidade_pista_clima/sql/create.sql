CREATE SEQUENCE IF NOT EXISTS "seq_letalidade_pista_clima" START 1;

CREATE TABLE IF NOT EXISTS "gold"."agg_letalidade_pista_clima" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_letalidade_pista_clima'),

    uf VARCHAR NOT NULL,
    br VARCHAR NOT NULL,
    area VARCHAR NOT NULL,
    tracado_via VARCHAR NOT NULL,
    tipo_via VARCHAR NOT NULL,
    condicao_metereologica VARCHAR NOT NULL,
    classificacao_acidente VARCHAR NOT NULL,

    total_ocorrencias BIGINT NOT NULL,
    pct_mortalidade DOUBLE PRECISION NOT NULL,

    CONSTRAINT "uq_agg_letalidade_pista_clima" UNIQUE (
        uf, 
        br, 
        area,
        tracado_via,
        tipo_via,
        condicao_metereologica,
        classificacao_acidente
    )
);
