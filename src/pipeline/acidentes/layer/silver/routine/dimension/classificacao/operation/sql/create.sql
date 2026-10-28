CREATE SEQUENCE IF NOT EXISTS "seq_dim_classificacao" START 1;

CREATE TABLE IF NOT EXISTS "silver"."dim_classificacao" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_dim_classificacao'),
    classificacao VARCHAR NOT NULL,
    CONSTRAINT "uq_dim_classificacao" UNIQUE (classificacao)
);