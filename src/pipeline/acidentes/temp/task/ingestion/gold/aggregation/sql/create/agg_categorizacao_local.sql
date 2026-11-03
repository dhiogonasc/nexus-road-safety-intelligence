CREATE SEQUENCE IF NOT EXISTS "seq_agg_categorizacao_local" START 1;

CREATE TABLE IF NOT EXISTS "gold"."agg_categorizacao_local" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_agg_categorizacao_local'),

    uf VARCHAR NOT NULL,
    br VARCHAR NOT NULL,
    km DOUBLE PRECISION NOT NULL,
    sentido VARCHAR NOT NULL,
    tipo_area VARCHAR NOT NULL,
    municipio VARCHAR NOT NULL,
    tipo_acidente VARCHAR NOT NULL,
    causa_acidente VARCHAR NOT NULL,
    classificacao_acidente VARCHAR NOT NULL,

    mortos BIGINT NOT NULL,
    total_ocorrencias BIGINT NOT NULL,
    pct_mortalidade DOUBLE PRECISION NOT NULL,

    CONSTRAINT "uq_agg_categorizacao_local" UNIQUE (
        uf, 
        br, 
        km, 
        sentido,
        tipo_area, 
        municipio,
        tipo_acidente,
        causa_acidente,
        classificacao_acidente
    )
);