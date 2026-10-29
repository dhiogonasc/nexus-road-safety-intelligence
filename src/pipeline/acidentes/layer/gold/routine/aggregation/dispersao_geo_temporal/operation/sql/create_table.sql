CREATE SEQUENCE IF NOT EXISTS "seq_dispersao_geo_temporal" START 1;

CREATE TABLE IF NOT EXISTS "gold"."agg_dispersao_geo_temporal" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_dispersao_geo_temporal'),

    uf VARCHAR NOT NULL,
    area VARCHAR NOT NULL,
    municipio VARCHAR NOT NULL,

    ano INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    dia_semana VARCHAR NOT NULL,

    total_ocorrencias BIGINT NOT NULL,
    total_pessoas BIGINT NOT NULL,
    total_veiculos BIGINT NOT NULL,
    total_mortos BIGINT NOT NULL,
    total_feridos BIGINT NOT NULL,
    total_feridos_graves BIGINT NOT NULL,
    total_feridos_leves BIGINT NOT NULL,
    total_ilesos BIGINT NOT NULL,

    pct_mortalidade DOUBLE PRECISION NOT NULL,

    CONSTRAINT "uq_agg_dispersao_geo_temporal" UNIQUE (
        uf, 
        area, 
        municipio,
        ano,
        mes, 
        dia_semana
    )
);
