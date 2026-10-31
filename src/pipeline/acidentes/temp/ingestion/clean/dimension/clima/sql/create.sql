CREATE SEQUENCE IF NOT EXISTS "seq_dim_clima" START 1 INCREMENT 1;

CREATE TABLE IF NOT EXISTS "silver"."dim_clima" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_dim_clima'),

    condicao VARCHAR NOT NULL,
    
    CONSTRAINT "uq_dim_clima" UNIQUE (condicao)
);