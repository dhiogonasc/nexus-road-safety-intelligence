CREATE SEQUENCE IF NOT EXISTS "seq_letalidade_pista_tempo" START 1;

CREATE TABLE IF NOT EXISTS "gold"."agg_letalidade_pista_tempo" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_letalidade_pista_tempo'),

    uf VARCHAR NOT NULL,
    br VARCHAR NOT NULL,
    km DOUBLE PRECISION NOT NULL,
    municipio VARCHAR NOT NULL,

    sentido_via VARCHAR NOT NULL,
    tracado_via VARCHAR NOT NULL,
    tipo_via VARCHAR NOT NULL,
    solo_via VARCHAR NOT NULL,

    mes INTEGER NOT NULL,
    dia_semana VARCHAR NOT NULL,
    fase_dia VARCHAR NOT NULL,

    causa_acidente VARCHAR NOT NULL,
    tipo_acidente VARCHAR NOT NULL,
    classificacao_acidente VARCHAR NOT NULL,

    total_ocorrencias BIGINT NOT NULL,
    total_pessoas BIGINT NOT NULL,
    total_veiculos BIGINT NOT NULL,
    total_mortos BIGINT NOT NULL,
    total_feridos BIGINT NOT NULL,
    total_feridos_graves BIGINT NOT NULL,
    total_feridos_leves BIGINT NOT NULL,
    total_ilesos BIGINT NOT NULL,

    pct_mortalidade DOUBLE PRECISION NOT NULL,

    CONSTRAINT "uq_agg_letalidade_pista_tempo" UNIQUE (
        uf, br, km, municipio,
        sentido_via,
        tracado_via,
        tipo_via,
        solo_via,
        mes, dia_semana, fase_dia,
        causa_acidente,
        tipo_acidente,
        classificacao_acidente
    )
);
