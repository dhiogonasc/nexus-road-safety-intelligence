CREATE TABLE IF NOT EXISTS "{catalog_name}"."core"."dim_categoria" (
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