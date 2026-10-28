CREATE SEQUENCE IF NOT EXISTS "seq_letalidade_clima_tempo" START 1;

CREATE TABLE IF NOT EXISTS "gold"."agg_letalidade_clima_tempo" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_letalidade_clima_tempo'),

    uf VARCHAR NOT NULL,
    municipio VARCHAR NOT NULL,

    condicao_metereologica VARCHAR NOT NULL,
    mes INTEGER NOT NULL,
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

    CONSTRAINT "uq_agg_letalidade_clima_tempo" UNIQUE (
        uf, municipio,
        condicao_metereologica,
        mes, fase_dia,
        causa_acidente,
        tipo_acidente,
        classificacao_acidente
    )
);
