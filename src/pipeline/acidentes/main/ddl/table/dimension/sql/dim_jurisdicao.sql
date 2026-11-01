CREATE TABLE IF NOT EXISTS "core"."dim_jurisdicao" (
    id INTEGER NOT NULL PRIMARY KEY,

    uop VARCHAR NOT NULL,
    regional VARCHAR NOT NULL,
    delegacia VARCHAR NOT NULL,
    
    CONSTRAINT "uq_dim_jurisdicao" UNIQUE (
        uop,
        regional,
        delegacia
    )
);

CREATE INDEX IF NOT EXISTS "idx_dim_jurisdicao_uop" ON "core"."dim_jurisdicao" (uop);