CREATE TABLE IF NOT EXISTS "{catalog_name}"."analytics"."agg_categorizacao_local" (
    id INTEGER NOT NULL PRIMARY KEY,

    uf VARCHAR NOT NULL,
    br VARCHAR NOT NULL,
    km DOUBLE PRECISION NOT NULL,
    sentido VARCHAR NOT NULL,
    tipo_area VARCHAR NOT NULL,
    municipio VARCHAR NOT NULL,
    tipo_acidente VARCHAR NOT NULL,
    causa_acidente VARCHAR NOT NULL,
    classificacao_acidente VARCHAR NOT NULL,

    mortos BIGINT NOT NULL,
    total_ocorrencias BIGINT NOT NULL,
    pct_mortalidade DOUBLE PRECISION NOT NULL,

    CONSTRAINT "uq_agg_categorizacao_local" UNIQUE (
        uf, 
        br, 
        km, 
        sentido,
        tipo_area, 
        municipio,
        tipo_acidente,
        causa_acidente,
        classificacao_acidente
    )
);

CREATE INDEX IF NOT EXISTS "idx_agg_categorizacao_local_uf" 
ON "{catalog_name}"."analytics"."agg_categorizacao_local" (uf);

CREATE INDEX IF NOT EXISTS "idx_agg_categorizacao_local_br" 
ON "{catalog_name}"."analytics"."agg_categorizacao_local" (br);

CREATE INDEX IF NOT EXISTS "idx_agg_categorizacao_local_uf_br" 
ON "{catalog_name}"."analytics"."agg_categorizacao_local" (uf, br);

CREATE INDEX IF NOT EXISTS "idx_agg_categorizacao_local_area" 
ON "{catalog_name}"."analytics"."agg_categorizacao_local" (tipo_area);

CREATE INDEX IF NOT EXISTS "idx_agg_categorizacao_local_uf_area" 
ON "{catalog_name}"."analytics"."agg_categorizacao_local" (uf, tipo_area);