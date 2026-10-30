CREATE TEMP TABLE temp_dim_local AS SELECT *
FROM read_parquet('{dim_local_storage_path}/**/*.parquet');

CREATE TEMP TABLE temp_dim_pista AS SELECT *
FROM read_parquet('{dim_pista_storage_path}/**/*.parquet');

CREATE TEMP TABLE temp_dim_clima AS SELECT *
FROM read_parquet('{dim_clima_storage_path}/**/*.parquet');

CREATE TEMP TABLE temp_dim_categoria AS SELECT *
FROM read_parquet('{dim_categoria_storage_path}/**/*.parquet');

SELECT setval(
    'seq_letalidade_pista_clima', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "gold"."agg_letalidade_pista_clima"), 0), 1)
);

CREATE TEMP TABLE temp_agg_letalidade_pista_clima AS
SELECT *
FROM (
    SELECT
        local.uf,
        local.br,
        local.area,
        pista.tracado AS tracado_via,
        pista.tipo AS tipo_via,
        clima.condicao AS condicao_metereologica,
        categoria.classificacao AS classificacao_acidente,
        CAST(COUNT(fato.id) AS BIGINT) AS total_ocorrencias,
        ROUND(CAST(SUM(fato.mortos) AS DOUBLE) / NULLIF(COUNT(fato.id), 0) * 100, 2) AS pct_mortalidade
    FROM
        "gold"."stg" AS fato
        JOIN temp_dim_local AS local ON fato.sk_local = local.id
        JOIN temp_dim_pista AS pista ON fato.sk_pista = pista.id
        JOIN temp_dim_clima AS clima ON fato.sk_clima = clima.id
        JOIN temp_dim_categoria AS categoria ON fato.sk_categoria = categoria.id     
    GROUP BY
        local.uf,
        local.br,
        local.area,
        pista.tracado,
        pista.tipo,
        clima.condicao,
        categoria.classificacao
);

MERGE INTO "gold"."agg_letalidade_pista_clima" AS target 
USING temp_agg_letalidade_pista_clima AS source 
    ON target.uf = source.uf
    AND target.br = source.br
    AND target.area = source.area
    AND target.tracado_via = source.tracado_via
    AND target.tipo_via = source.tipo_via
    AND target.condicao_metereologica = source.condicao_metereologica
    AND target.classificacao_acidente = source.classificacao_acidente

WHEN MATCHED THEN
UPDATE SET
    total_ocorrencias = source.total_ocorrencias,
    pct_mortalidade = source.pct_mortalidade

WHEN NOT MATCHED THEN 
INSERT (
    id,
    uf, 
    br,
    area,
    tracado_via,
    tipo_via,
    condicao_metereologica,
    classificacao_acidente,
    total_ocorrencias,
    pct_mortalidade
) 
VALUES (
    nextval('seq_letalidade_pista_clima'),
    source.uf, 
    source.br,
    source.area,
    source.tracado_via,
    source.tipo_via,
    source.condicao_metereologica,
    source.classificacao_acidente,
    source.total_ocorrencias,
    source.pct_mortalidade
);

DROP TABLE IF EXISTS temp_dim_local;
DROP TABLE IF EXISTS temp_dim_pista;
DROP TABLE IF EXISTS temp_dim_clima;
DROP TABLE IF EXISTS temp_dim_categoria;
DROP TABLE IF EXISTS temp_agg_letalidade_pista_clima;