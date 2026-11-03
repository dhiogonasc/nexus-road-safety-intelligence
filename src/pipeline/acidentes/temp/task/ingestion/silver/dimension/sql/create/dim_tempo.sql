CREATE SEQUENCE IF NOT EXISTS "seq_dim_tempo" START;

CREATE TABLE IF NOT EXISTS "silver"."dim_tempo" (
    id INTEGER NOT NULL PRIMARY KEY,

    ano INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    semana INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL,
    fase_dia INTEGER NOT NULL,

    -- colunas de exibição
    mes_str VARCHAR NOT NULL,
    dia_semana_str VARCHAR NOT NULL,
    fase_dia_str VARCHAR NOT NULL,

    CONSTRAINT "uq_dim_tempo" UNIQUE (
        ano,
        mes,
        semana,
        dia_semana,
        fase_dia
    )
);
