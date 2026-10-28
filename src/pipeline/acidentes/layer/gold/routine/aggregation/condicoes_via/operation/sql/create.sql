CREATE SEQUENCE IF NOT EXISTS "seq_condicoes_via" START 1;

CREATE TABLE "gold"."condicoes_via" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_condicoes_via'),

    ano INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    dia INTEGER NOT NULL,
    dia_semana VARCHAR NOT NULL,
    fase_dia VARCHAR NOT NULL,

    condicao_metereologica VARCHAR NOT NULL,
    
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

    CONSTRAINT "uq_agg_condicoes_via" UNIQUE (
        ano, mes, dia, 
        dia_semana, fase_dia, 
        condicao_metereologica, 
        sentido_via, tracado_via, 
        tipo_via, solo_via
    )
);

CREATE INDEX IF NOT EXISTS "idx_agg_condicoes_via_temporal" ON "gold"."condicoes_via" (ano, mes, dia);
CREATE INDEX IF NOT EXISTS "idx_agg_condicoes_via_climatica" ON "gold"."condicoes_via" (condicao_metereologica, fase_dia);

