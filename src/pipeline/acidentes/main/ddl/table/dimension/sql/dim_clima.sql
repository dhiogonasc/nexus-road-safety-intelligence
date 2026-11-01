CREATE TABLE IF NOT EXISTS "{catalog_name}"."core"."dim_clima" (
    id INTEGER NOT NULL PRIMARY KEY,

    condicao VARCHAR NOT NULL,
    
    CONSTRAINT "uq_dim_clima" UNIQUE (condicao)
);