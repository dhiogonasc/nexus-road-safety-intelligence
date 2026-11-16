CREATE TABLE IF NOT EXISTS "gold"."agg_categorizacao_local" (
    id VARCHAR NOT NULL PRIMARY KEY,

    uf VARCHAR NOT NULL,
    br INTEGER NOT NULL,
    km DECIMAL(5, 3) NOT NULL,
    sentido VARCHAR NOT NULL,
    tipo_area VARCHAR NOT NULL,
    municipio VARCHAR NOT NULL,

    -- categorizacao
    tipo_acidente VARCHAR NOT NULL,
    causa_acidente VARCHAR NOT NULL,
    classificacao_acidente VARCHAR NOT NULL,


    -- variaveis
    total_mortos BIGINT NOT NULL,
    total_envolvidos BIGINT NOT NULL,
    total_ocorrencias BIGINT NOT NULL,

    -- metricas
    taxa_mortalidade_por_ocorrencia DECIMAL(5, 2) NOT NULL,
    taxa_mortalidade_por_envolvido DECIMAL(5, 2) NOT NULL,

    CONSTRAINT "uq_agg_categorizacao_local" UNIQUE (
        uf, 
        br, 
        km, 
        sentido,
        tipo_area, 
        municipio,
        tipo_acidente,
        causa_acidente,
        classificacao_acidente
    )
);