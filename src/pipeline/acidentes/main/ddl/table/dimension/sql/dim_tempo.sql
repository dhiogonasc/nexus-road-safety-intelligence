CREATE TABLE IF NOT EXISTS "core"."dim_tempo" (
    id INTEGER NOT NULL PRIMARY KEY,

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

CREATE INDEX IF NOT EXISTS "idx_dim_tempo_ano" ON "core"."dim_tempo" (ano);
