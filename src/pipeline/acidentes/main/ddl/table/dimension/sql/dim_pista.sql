CREATE TABLE IF NOT EXISTS "core"."dim_pista" (
    id INTEGER NOT NULL PRIMARY KEY,

    tracado VARCHAR NOT NULL,
    tipo VARCHAR NOT NULL,

    CONSTRAINT "uq_dim_pista" UNIQUE (
        tracado, 
        tipo
    )
);