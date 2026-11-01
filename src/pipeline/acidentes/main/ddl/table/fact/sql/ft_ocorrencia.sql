CREATE TABLE IF NOT EXISTS "core"."ft_ocorrencia" (
    id INTEGER NOT NULL PRIMARY KEY,

    id_ocorrencia BIGINT NOT NULL,
    sk_tempo INTEGER NOT NULL,
    sk_local INTEGER NOT NULL,
    sk_pista INTEGER NOT NULL,
    sk_jurisdicao INTEGER NOT NULL,
    sk_clima INTEGER NOT NULL,
    sk_categoria INTEGER NOT NULL,
    
    pessoas INTEGER NOT NULL,
    mortos INTEGER NOT NULL,
    feridos_leves INTEGER NOT NULL,
    feridos_graves INTEGER NOT NULL,
    feridos INTEGER NOT NULL,
    ilesos INTEGER NOT NULL,
    ignorados INTEGER NOT NULL,
    veiculos INTEGER NOT NULL,

    CONSTRAINT "fk_ft_ocorrencia_tempo" FOREIGN KEY (sk_tempo) REFERENCES "core"."dim_tempo" (id),
    CONSTRAINT "fk_ft_ocorrencia_local" FOREIGN KEY (sk_local) REFERENCES "core"."dim_local" (id),
    CONSTRAINT "fk_ft_ocorrencia_pista" FOREIGN KEY (sk_pista) REFERENCES "core"."dim_pista" (id),
    CONSTRAINT "fk_ft_ocorrencia_jurisdicao" FOREIGN KEY (sk_jurisdicao) REFERENCES "core"."dim_jurisdicao" (id),
    CONSTRAINT "fk_ft_ocorrencia_clima" FOREIGN KEY (sk_clima) REFERENCES "core"."dim_clima" (id),
    CONSTRAINT "fk_ft_ocorrencia_categoria" FOREIGN KEY (sk_categoria) REFERENCES "core"."dim_categoria" (id),

    CONSTRAINT "uq_ft_ocorrencia" UNIQUE (
        id_ocorrencia,
        sk_tempo,
        sk_local,
        sk_pista,
        sk_jurisdicao,
        sk_clima,
        sk_categoria
    )
);