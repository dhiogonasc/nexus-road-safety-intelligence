CREATE SEQUENCE IF NOT EXISTS "seq_letalidade_clima_tempo" START 1;

CREATE TABLE IF NOT EXISTS "gold"."agg_letalidade_clima_tempo" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_letalidade_clima_tempo'),

    uf VARCHAR NOT NULL,
    area VARCHAR NOT NULL,
    condicao_metereologica VARCHAR NOT NULL,
    mes INTEGER NOT NULL,
    fase_dia VARCHAR NOT NULL,
    classificacao_acidente VARCHAR NOT NULL,
    total_ocorrencias BIGINT NOT NULL,
    pct_mortalidade DOUBLE PRECISION NOT NULL,

    CONSTRAINT "uq_agg_letalidade_clima_tempo" UNIQUE (
        uf, 
        area,
        condicao_metereologica,
        mes, 
        fase_dia,
        classificacao_acidente
    )
);
