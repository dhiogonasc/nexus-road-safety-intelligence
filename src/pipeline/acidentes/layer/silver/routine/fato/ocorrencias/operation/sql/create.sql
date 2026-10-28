CREATE SEQUENCE IF NOT EXISTS "seq_ft_ocorrencia" START 1;

CREATE TABLE IF NOT EXISTS "silver"."ft_ocorrencia" (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('seq_ft_ocorrencia'),

    id_ocorrencia BIGINT NOT NULL,
    sk_tempo INTEGER NOT NULL,
    sk_localizacao INTEGER NOT NULL,
    sk_coordenada INTEGER NOT NULL,
    sk_causa INTEGER NOT NULL,
    sk_tipo INTEGER NOT NULL,
    sk_classificacao INTEGER NOT NULL,
    sk_pista INTEGER NOT NULL,
    sk_condicao_metereologica INTEGER NOT NULL,
    
    pessoas INTEGER NOT NULL,
    mortos INTEGER NOT NULL,
    feridos_leves INTEGER NOT NULL,
    feridos_graves INTEGER NOT NULL,
    feridos INTEGER NOT NULL,
    ilesos INTEGER NOT NULL,
    ignorados INTEGER NOT NULL,
    veiculos INTEGER NOT NULL,

    CONSTRAINT "uq_ft_ocorrencia" UNIQUE (
        id_ocorrencia,
        sk_tempo,
        sk_localizacao,
        sk_coordenada,
        sk_causa,
        sk_tipo,
        sk_classificacao,
        sk_pista,
        sk_condicao_metereologica
    )
);

CREATE INDEX IF NOT EXISTS "idx_ft_ocorrencia_tempo" ON "silver"."ft_ocorrencia" (sk_tempo);
CREATE INDEX IF NOT EXISTS "idx_ft_ocorrencia_localizacao" ON "silver"."ft_ocorrencia" (sk_localizacao);
CREATE INDEX IF NOT EXISTS "idx_ft_ocorrencia_causa" ON "silver"."ft_ocorrencia" (sk_causa);
CREATE INDEX IF NOT EXISTS "idx_ft_ocorrencia_condicao_metereologica" ON "silver"."ft_ocorrencia" (sk_condicao_metereologica);