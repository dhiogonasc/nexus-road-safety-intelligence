CREATE TEMP TABLE temp_dim_local AS SELECT *
FROM read_parquet('{dim_local_storage_path}/**/*.parquet');

CREATE TEMP TABLE temp_dim_pista AS SELECT *
FROM read_parquet('{dim_pista_storage_path}/**/*.parquet');

CREATE TEMP TABLE temp_dim_categoria AS SELECT *
FROM read_parquet('{dim_categoria_storage_path}/**/*.parquet');

SELECT setval(
    'seq_trechos_criticos', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "gold"."agg_trechos_criticos"), 0), 1)
);

CREATE TEMP TABLE temp_agg_trechos_criticos AS
SELECT *
FROM (
    SELECT
        local.uf,
        local.br,
        local.km,
        local.sentido,
        local.area,
        pista.tracado as tracado_via,
        pista.tipo as tipo_via,
        categoria.classificacao as classificacao_acidente,
        CAST(COUNT(fato.id) AS BIGINT) AS total_ocorrencias,
        ROUND(CAST(SUM(fato.mortos) AS DOUBLE) / NULLIF(COUNT(fato.id), 0) * 100, 2) AS pct_mortalidade
    FROM
        "gold"."stg_ft_ocorrencia" AS fato
        JOIN temp_dim_local AS local ON fato.sk_local = local.id
        JOIN temp_dim_pista AS pista ON fato.sk_pista = pista.id
        JOIN temp_dim_categoria AS categoria ON fato.sk_categoria = categoria.id
    GROUP BY
        local.uf,
        local.br,
        local.km,
        local.sentido,
        local.area,
        pista.tracado,
        pista.tipo,
        categoria.classificacao
);

MERGE INTO "gold"."agg_trechos_criticos" AS target 
USING temp_agg_trechos_criticos AS source 
    ON target.uf = source.uf
    AND target.br = source.br
    AND target.km = source.km
    AND target.sentido = source.sentido
    AND target.area = source.area
    AND target.tracado_via = source.tracado_via
    AND target.tipo_via = source.tipo_via
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
    km,
    sentido,
    area,
    tracado_via,
    tipo_via,
    classificacao_acidente,
    total_ocorrencias,
    pct_mortalidade
) 
VALUES (
    nextval('seq_trechos_criticos'),
    source.uf, 
    source.br, 
    source.km,
    source.sentido,
    source.area,
    source.tracado_via,
    source.tipo_via,
    source.classificacao_acidente,
    source.total_ocorrencias,
    source.pct_mortalidade
);

DROP TABLE IF EXISTS temp_dim_local;
DROP TABLE IF EXISTS temp_dim_pista;
DROP TABLE IF EXISTS temp_dim_categoria;
DROP TABLE IF EXISTS temp_agg_trechos_criticos;