CREATE SEQUENCE IF NOT EXISTS "seq_dim_pista" START 1 INCREMENT 1;

CREATE TABLE IF NOT EXISTS "silver"."dim_pista" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_dim_pista'),

    tracado VARCHAR NOT NULL,
    tipo VARCHAR NOT NULL,

    CONSTRAINT "uq_dim_pista" UNIQUE (
        tracado, 
        tipo
    )
);