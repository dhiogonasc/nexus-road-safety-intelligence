CREATE TABLE IF NOT EXISTS "analytics"."agg_trechos_criticos" (
    id INTEGER NOT NULL PRIMARY KEY,

    uf VARCHAR NOT NULL,
    br VARCHAR NOT NULL,
    km DOUBLE PRECISION NOT NULL,
    sentido VARCHAR NOT NULL,
    area VARCHAR NOT NULL,
    tracado_via VARCHAR NOT NULL,
    tipo_via VARCHAR NOT NULL,
    classificacao_acidente VARCHAR NOT NULL,

    total_ocorrencias BIGINT NOT NULL,
    pct_mortalidade DOUBLE PRECISION NOT NULL,

    CONSTRAINT "uq_agg_trechos_criticos" UNIQUE (
        uf, 
        br, 
        km, 
        sentido,
        area, 
        tracado_via,
        tipo_via,
        classificacao_acidente
    )
);

CREATE INDEX IF NOT EXISTS "idx_agg_trechos_criticos_uf_br" ON "analytics"."agg_trechos_criticos" (uf, br);
