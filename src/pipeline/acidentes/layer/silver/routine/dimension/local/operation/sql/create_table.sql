CREATE SEQUENCE IF NOT EXISTS "seq_dim_local" START 1 INCREMENT 1;

CREATE TABLE IF NOT EXISTS "silver"."dim_local" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_dim_local'),
    
    uf VARCHAR NOT NULL,
    br VARCHAR NOT NULL,
    km DOUBLE PRECISION NOT NULL,
    sentido VARCHAR NOT NULL,
    municipio VARCHAR NOT NULL,
    area VARCHAR NOT NULL
    
    CONSTRAINT "uq_dim_local" UNIQUE (
        uf, 
        br, 
        km, 
        sentido, 
        municipio, 
        area
    )
);
