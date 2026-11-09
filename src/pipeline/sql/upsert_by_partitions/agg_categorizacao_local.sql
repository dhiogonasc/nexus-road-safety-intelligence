MERGE INTO "gold"."agg_categorizacao_local" AS target 
USING (
    SELECT 
        md5(
            COALESCE(CAST(local.uf AS VARCHAR), '0') || '-' ||
            COALESCE(CAST(local.br AS VARCHAR), '0') || '-' ||
            COALESCE(CAST(local.km AS VARCHAR), '0') || '-' ||
            COALESCE(CAST(local.sentido AS VARCHAR), '0') || '-' ||
            COALESCE(CAST(local.tipo_area AS VARCHAR), '0') || '-' ||
            COALESCE(CAST(local.municipio AS VARCHAR), '0') || '-' ||
            COALESCE(CAST(categoria.tipo AS VARCHAR), '0') || '-' ||
            COALESCE(CAST(categoria.causa AS VARCHAR), '0') || '-' ||
            COALESCE(CAST(categoria.classificacao AS VARCHAR), '0')
        ) AS id,
        local.uf, 
        local.br, 
        local.km, 
        local.sentido,
        local.tipo_area, 
        local.municipio,
        categoria.tipo AS tipo_acidente,
        categoria.causa AS causa_acidente,
        categoria.classificacao AS classificacao_acidente,
        CAST(SUM(fato.mortos) AS BIGINT) AS total_mortos,
        CAST(SUM(fato.pessoas) AS BIGINT) AS total_envolvidos,
        CAST(COUNT(fato.id_ocorrencia) AS BIGINT) AS total_ocorrencias,
        ROUND(
            CAST(SUM(fato.mortos) AS DECIMAL(5, 2)) 
            / NULLIF(CAST(SUM(fato.pessoas) AS DECIMAL(5, 2)), 0), 4
        ) AS taxa_mortalidade_por_envolvido,
        ROUND(
            CAST(SUM(fato.mortos) AS DECIMAL(5, 2)) 
            / NULLIF(CAST(COUNT(fato.id_ocorrencia) AS DECIMAL(5, 2)), 0), 4
        ) AS taxa_mortalidade_por_ocorrencia
    FROM (
        SELECT *
        FROM read_parquet(
            '{fct_ocorrencia_storage_path}/**/*.parquet', 
            hive_partitioning = true
        )
    ) AS fato
    JOIN (
        SELECT *
        FROM read_parquet('{dim_local_storage_path}/**/*.parquet')
    ) AS local ON fato.sk_local = local.id
    JOIN (
        SELECT *
        FROM read_parquet('{dim_categoria_storage_path}/**/*.parquet')
    ) AS categoria ON fato.sk_categoria = categoria.id
    WHERE 1=1
    {filter_clause}
    GROUP BY
        local.uf, 
        local.br, 
        local.km, 
        local.sentido,
        local.tipo_area, 
        local.municipio,
        categoria.tipo,
        categoria.causa,
        categoria.classificacao
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
    total_mortos = source.total_mortos,
    total_envolvidos = source.total_envolvidos,
    total_ocorrencias = source.total_ocorrencias,
    taxa_mortalidade_por_envolvido = source.taxa_mortalidade_por_envolvido,
    taxa_mortalidade_por_ocorrencia = source.taxa_mortalidade_por_ocorrencia

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
    total_mortos,
    total_envolvidos,
    total_ocorrencias,
    taxa_mortalidade_por_envolvido,
    taxa_mortalidade_por_ocorrencia
) 
VALUES (
    source.id,
    source.uf, 
    source.br, 
    source.km, 
    source.sentido,
    source.tipo_area, 
    source.municipio,
    source.tipo_acidente,
    source.causa_acidente,
    source.classificacao_acidente,
    source.total_mortos,
    source.total_envolvidos,
    source.total_ocorrencias,
    source.taxa_mortalidade_por_envolvido,
    source.taxa_mortalidade_por_ocorrencia
);