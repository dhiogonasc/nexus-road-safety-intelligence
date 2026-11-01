CREATE TABLE IF NOT EXISTS "{catalog_name}"."analytics"."agg_letalidade_clima_tempo" (
    id INTEGER NOT NULL PRIMARY KEY,

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

CREATE INDEX IF NOT EXISTS "idx_agg_letalidade_clima_tempo_condicao_metereologica" ON "{catalog_name}"."analytics"."agg_letalidade_clima_tempo" (condicao_metereologica);
CREATE INDEX IF NOT EXISTS "idx_agg_letalidade_clima_tempo_uf" ON "{catalog_name}"."analytics"."agg_letalidade_clima_tempo" (uf);
