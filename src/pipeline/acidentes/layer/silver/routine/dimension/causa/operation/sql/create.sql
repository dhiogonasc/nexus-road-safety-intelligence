CREATE SEQUENCE IF NOT EXISTS "seq_dim_causa" START 1;

CREATE TABLE IF NOT EXISTS "silver"."dim_causa" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_dim_causa'),
    causa VARCHAR NOT NULL,
    CONSTRAINT "uq_dim_causa" UNIQUE (causa)
);
