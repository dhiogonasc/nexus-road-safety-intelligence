CREATE SEQUENCE IF NOT EXISTS "seq_trechos_criticos" START 1;

CREATE TABLE IF NOT EXISTS "gold"."agg_trechos_criticos" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_trechos_criticos'),

    uf VARCHAR NOT NULL,
    br VARCHAR NOT NULL,
    km DOUBLE PRECISION NOT NULL,
    uop VARCHAR NOT NULL,
    regional VARCHAR NOT NULL,
    municipio VARCHAR NOT NULL,
    delegacia VARCHAR NOT NULL,

    sentido_via VARCHAR NOT NULL,
    tracado_via VARCHAR NOT NULL,
    tipo_via VARCHAR NOT NULL,
    solo_via VARCHAR NOT NULL, 

    total_ocorrencias BIGINT NOT NULL,
    total_pessoas BIGINT NOT NULL,
    total_veiculos BIGINT NOT NULL,
    total_mortos BIGINT NOT NULL,
    total_feridos BIGINT NOT NULL,
    total_feridos_graves BIGINT NOT NULL,
    total_feridos_leves BIGINT NOT NULL,
    total_ilesos BIGINT NOT NULL,

    pct_mortalidade DOUBLE PRECISION NOT NULL,

    CONSTRAINT "uq_agg_trechos_criticos" UNIQUE (
        uf, br, km, uop,
        regional, 
        municipio, 
        delegacia,
        sentido_via,
        tracado_via,
        tipo_via,
        solo_via
    )
);
