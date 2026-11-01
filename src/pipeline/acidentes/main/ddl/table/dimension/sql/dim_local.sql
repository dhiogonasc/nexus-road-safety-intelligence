CREATE TABLE IF NOT EXISTS "{catalog_name}"."core"."dim_local" (
    id INTEGER NOT NULL PRIMARY KEY,
    
    uf VARCHAR NOT NULL,
    br VARCHAR NOT NULL,
    km DOUBLE PRECISION NOT NULL,
    sentido VARCHAR NOT NULL,
    municipio VARCHAR NOT NULL,
    area VARCHAR NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    
    CONSTRAINT "uq_dim_local" UNIQUE (
        uf, 
        br, 
        km, 
        sentido, 
        municipio, 
        area,
        latitude,
        longitude
    )
);

CREATE INDEX IF NOT EXISTS "idx_dim_local_uf" ON "{catalog_name}"."core"."dim_local" (uf);
