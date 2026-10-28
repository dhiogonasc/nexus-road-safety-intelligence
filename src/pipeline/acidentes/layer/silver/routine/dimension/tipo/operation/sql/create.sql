CREATE SEQUENCE IF NOT EXISTS "seq_dim_tipo" START 1;

CREATE TABLE IF NOT EXISTS "silver"."dim_tipo" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_dim_tipo'),
    tipo VARCHAR NOT NULL,
    CONSTRAINT "uq_dim_tipo" UNIQUE (tipo)
);