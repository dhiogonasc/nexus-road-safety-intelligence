CREATE SEQUENCE IF NOT EXISTS "seq_dim_tempo" START 1;

CREATE TABLE IF NOT EXISTS "silver"."dim_tempo" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_dim_tempo'),

    data_hora TIMESTAMP NOT NULL,
    ano INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    dia INTEGER NOT NULL,
    hora INTEGER NOT NULL,
    dia_semana VARCHAR NOT NULL,
    fase_dia VARCHAR NOT NULL,

    CONSTRAINT "uq_dim_tempo" UNIQUE (
        data_hora,
        dia_semana,
        fase_dia
    )
);
