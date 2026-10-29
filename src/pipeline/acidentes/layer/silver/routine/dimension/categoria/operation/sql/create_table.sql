CREATE SEQUENCE IF NOT EXISTS "seq_dim_categoria" START 1 INCREMENT 1;

CREATE TABLE IF NOT EXISTS "silver"."dim_categoria" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_dim_categoria'),

    classificacao VARCHAR NOT NULL,
    causa VARCHAR NOT NULL,
    tipo VARCHAR NOT NULL,
    
    CONSTRAINT "uq_dim_categoria" UNIQUE (
        classificacao,
        causa,
        tipo
    )
);