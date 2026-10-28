CREATE SEQUENCE IF NOT EXISTS "seq_condicoes_via" START 1;

CREATE TABLE "gold"."condicoes_via" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_condicoes_via'),

    ano INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    dia INTEGER NOT NULL,
    dia_semana VARCHAR NOT NULL,
    fase_dia VARCHAR NOT NULL,



    total_ocorrencias BIGINT NOT NULL,
    total_pessoas BIGINT NOT NULL,
    total_veiculos BIGINT NOT NULL,
    total_mortos BIGINT NOT NULL,
    total_feridos BIGINT NOT NULL,
    total_feridos_graves BIGINT NOT NULL,
    total_feridos_leves BIGINT NOT NULL,
    total_ilesos BIGINT NOT NULL,

    pct_mortalidade DOUBLE PRECISION NOT NULL,

    CONSTRAINT "uq_agg_condicoes_via" UNIQUE (
        ano, mes, dia, 
        dia_semana, fase_dia, 

    )
);

CREATE INDEX IF NOT EXISTS "idx_agg_condicoes_via_temporal" ON "gold"."condicoes_via" (ano, mes, dia);

