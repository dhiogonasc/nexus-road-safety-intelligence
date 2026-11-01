CREATE TABLE IF NOT EXISTS "analytics"."agg_dispersao_geo_temporal" (
    id INTEGER NOT NULL PRIMARY KEY,

    uf VARCHAR NOT NULL,
    area VARCHAR NOT NULL,
    municipio VARCHAR NOT NULL,
    ano INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    dia_semana VARCHAR NOT NULL,
    
    total_ocorrencias BIGINT NOT NULL,
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

CREATE INDEX IF NOT EXISTS "idx_agg_dispersao_geo_temporal_uf" ON "analytics"."agg_dispersao_geo_temporal" (uf);
