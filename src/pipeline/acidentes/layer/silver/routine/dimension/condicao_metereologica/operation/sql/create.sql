CREATE SEQUENCE IF NOT EXISTS "seq_dim_condicao_metereologica" START 1;

CREATE TABLE IF NOT EXISTS "silver"."dim_condicao_metereologica" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_dim_condicao_metereologica'),
    condicao VARCHAR NOT NULL,
    CONSTRAINT "uq_dim_condicao_metereologica" UNIQUE (condicao)
);