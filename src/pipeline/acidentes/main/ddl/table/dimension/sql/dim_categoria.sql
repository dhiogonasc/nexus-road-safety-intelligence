CREATE TABLE IF NOT EXISTS "core"."dim_categoria" (
    id INTEGER NOT NULL PRIMARY KEY,

    classificacao VARCHAR NOT NULL,
    causa VARCHAR NOT NULL,
    tipo VARCHAR NOT NULL,
    
    CONSTRAINT "uq_dim_categoria" UNIQUE (
        classificacao,
        causa,
        tipo
    )
);

CREATE INDEX IF NOT EXISTS "idx_dim_categoria_classificacao" ON "core"."dim_categoria" (classificacao);