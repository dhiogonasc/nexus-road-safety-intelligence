CREATE SEQUENCE IF NOT EXISTS "seq_letalidade_pista_tempo" START 1;

CREATE TABLE IF NOT EXISTS "gold"."agg_letalidade_pista_tempo" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_letalidade_pista_tempo'),

    uf VARCHAR NOT NULL,
    br VARCHAR NOT NULL,
    area VARCHAR NOT NULL,
    tracado_via VARCHAR NOT NULL,
    tipo_via VARCHAR NOT NULL,
    mes INTEGER NOT NULL,
    dia_semana VARCHAR NOT NULL,
    fase_dia VARCHAR NOT NULL,
    classificacao_acidente VARCHAR NOT NULL,

    total_ocorrencias BIGINT NOT NULL,
    pct_mortalidade DOUBLE PRECISION NOT NULL,

    CONSTRAINT "uq_agg_letalidade_pista_tempo" UNIQUE (
        uf, 
        br, 
        area,
        tracado_via,
        tipo_via,
        mes, 
        dia_semana, 
        fase_dia,
        classificacao_acidente
    )
);
