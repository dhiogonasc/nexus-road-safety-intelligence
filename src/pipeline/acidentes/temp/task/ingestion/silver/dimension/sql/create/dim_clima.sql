CREATE SEQUENCE IF NOT EXISTS "seq_dim_clima" START;

CREATE TABLE IF NOT EXISTS "silver"."dim_clima" (
    id INTEGER NOT NULL PRIMARY KEY,

    condicao VARCHAR NOT NULL,
    
    CONSTRAINT "uq_dim_clima" UNIQUE (condicao)
);