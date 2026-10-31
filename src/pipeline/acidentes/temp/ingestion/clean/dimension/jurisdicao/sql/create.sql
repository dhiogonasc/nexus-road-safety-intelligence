CREATE SEQUENCE IF NOT EXISTS "seq_dim_jurisdicao" START 1 INCREMENT 1;

CREATE TABLE IF NOT EXISTS "silver"."dim_jurisdicao" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_dim_jurisdicao'),

    uop VARCHAR NOT NULL,
    regional VARCHAR NOT NULL,
    delegacia VARCHAR NOT NULL,
    
    CONSTRAINT "uq_dim_jurisdicao" UNIQUE (
        uop,
        regional,
        delegacia
    )
);