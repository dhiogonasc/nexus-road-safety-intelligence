CREATE TABLE IF NOT EXISTS "{catalog_name}"."core"."dim_tempo" (
    id INTEGER NOT NULL PRIMARY KEY,

    ano INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    semana INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL,
    fase_dia INTEGER NOT NULL,

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
