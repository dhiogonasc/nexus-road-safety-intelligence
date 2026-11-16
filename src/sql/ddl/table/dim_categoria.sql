CREATE SEQUENCE IF NOT EXISTS "seq_dim_categoria";

CREATE TABLE IF NOT EXISTS "silver"."dim_categoria" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_dim_categoria'),

    tipo VARCHAR NOT NULL,
    causa VARCHAR NOT NULL,
    classificacao VARCHAR NOT NULL,
    
    CONSTRAINT "uq_dim_categoria" UNIQUE (
        tipo,
        causa,
        classificacao
    )
);