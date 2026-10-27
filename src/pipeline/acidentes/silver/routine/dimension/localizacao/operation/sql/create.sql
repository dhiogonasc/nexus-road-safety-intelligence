CREATE SEQUENCE IF NOT EXISTS "seq_dim_localizacao" START 1;

CREATE TABLE IF NOT EXISTS "silver"."dim_localizacao" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_dim_localizacao'),
    uf VARCHAR NOT NULL,
    br VARCHAR NOT NULL,
    km DOUBLE PRECISION NOT NULL,
    municipio VARCHAR NOT NULL,
    regional VARCHAR NOT NULL,
    delegacia VARCHAR NOT NULL,
    uop VARCHAR NOT NULL,
    
    CONSTRAINT "uq_dim_localizacao" UNIQUE (
        uf, br, km, uop, 
        municipio, 
        regional, 
        delegacia
    )
);

CREATE INDEX IF NOT EXISTS "idx_dim_localizacao" ON "silver"."dim_localizacao" (uf);
