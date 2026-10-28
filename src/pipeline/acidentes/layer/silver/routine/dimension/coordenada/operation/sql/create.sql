CREATE SEQUENCE IF NOT EXISTS "seq_dim_coordenada" START 1;

CREATE TABLE IF NOT EXISTS "silver"."dim_coordenada" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_dim_coordenada'),
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    CONSTRAINT "uq_dim_coordenada" UNIQUE (latitude, longitude)
);