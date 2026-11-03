SELECT setval(
    'seq_agg_categorizacao_local', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "gold"."agg_categorizacao_local"), 0), 1)
);

MERGE INTO "gold"."agg_categorizacao_local" AS target 
USING (
    SELECT
        local.uf, 
        local.br, 
        local.km, 
        local.sentido,
        local.tipo_area, 
        local.municipio,
        categoria.tipo_acidente,
        categoria.causa_acidente,
        categoria.classificacao_acidente,
        CAST(SUM(fato.mortos) AS DOUBLE) AS mortos,
        CAST(COUNT(fato.id) AS BIGINT) AS total_ocorrencias,
        ROUND(CAST(SUM(fato.mortos) AS DOUBLE) / NULLIF(COUNT(fato.id), 0) * 100, 2) AS pct_mortalidade
    FROM
        "gold"."stg_ft_ocorrencia" AS fato
        JOIN (
            SELECT *
            FROM read_parquet('{dim_local_storage_path}/**/*.parquet');
        ) AS local ON fato.sk_local = local.id
        JOIN (
            SELECT *
            FROM read_parquet('{dim_categoria_storage_path}/**/*.parquet');
        ) AS categoria ON fato.sk_categoria = categoria.id
    GROUP BY
        local.uf, 
        local.br, 
        local.km, 
        local.sentido,
        local.tipo_area, 
        local.municipio,
        categoria.tipo_acidente,
        categoria.causa_acidente,
        categoria.classificacao_acidente
) AS source 
    ON target.uf = source.uf
    AND target.br = source.br
    AND target.km = source.km
    AND target.sentido = source.sentido
    AND target.tipo_area = source.tipo_area
    AND target.municipio = source.municipio
    AND target.tipo_acidente = source.tipo_acidente
    AND target.causa_acidente = source.causa_acidente
    AND target.classificacao_acidente = source.classificacao_acidente

WHEN MATCHED THEN
UPDATE SET
    mortos =  source.mortos,
    total_ocorrencias = source.total_ocorrencias,
    pct_mortalidade = source.pct_mortalidade

WHEN NOT MATCHED THEN 
INSERT (
    id,
    uf, 
    br, 
    km, 
    sentido,
    tipo_area, 
    municipio,
    tipo_acidente,
    causa_acidente,
    classificacao_acidente,
    mortos,
    total_ocorrencias,
    pct_mortalidade
) 
VALUES (
    nextval('seq_agg_categorizacao_local'),
    source.uf, 
    source.br, 
    source.km, 
    source.sentido,
    source.tipo_area, 
    source.municipio,
    source.tipo_acidente,
    source.causa_acidente,
    source.classificacao_acidente,
    source.mortos,
    source.total_ocorrencias,
    source.pct_mortalidade
);