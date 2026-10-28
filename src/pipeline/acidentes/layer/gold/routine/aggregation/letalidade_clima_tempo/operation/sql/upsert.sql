CREATE TEMP TABLE temp_dim_localizacao AS SELECT *
FROM read_parquet('{dim_localizacao_storage_path}/**/*.parquet');

CREATE TEMP TABLE temp_dim_condicao_metereologica AS SELECT *
FROM read_parquet('{dim_condicao_metereologica_storage_path}/**/*.parquet');

CREATE TEMP TABLE temp_dim_tempo AS SELECT *
FROM read_parquet('{dim_tempo_storage_path}/**/*.parquet');

CREATE TEMP TABLE temp_dim_causa AS SELECT *
FROM read_parquet('{dim_causa_storage_path}/**/*.parquet');

CREATE TEMP TABLE temp_dim_tipo AS SELECT *
FROM read_parquet('{dim_tipo_storage_path}/**/*.parquet');

CREATE TEMP TABLE temp_dim_classificacao AS SELECT *
FROM read_parquet('{dim_classificacao_storage_path}/**/*.parquet');

SELECT setval(
    'seq_letalidade_clima_tempo', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "gold"."agg_letalidade_clima_tempo"), 0), 1)
);

CREATE TEMP TABLE temp_agg_letalidade_clima_tempo AS
SELECT nextval('seq_letalidade_clima_tempo') AS id, *
FROM (
    SELECT
        localizacao.uf,
        localizacao.municipio,

        condicao_metereologica.condicao AS condicao_metereologica,
        tempo.mes,
        tempo.fase_dia,

        causa.causa AS causa_acidente,
        tipo.tipo AS tipo_acidente,
        classificacao.classificacao AS classificacao_acidente,

        CAST(COUNT(fato.id) AS BIGINT) AS total_ocorrencias,
        CAST(SUM(fato.pessoas) AS BIGINT) AS total_pessoas,
        CAST(SUM(fato.veiculos) AS BIGINT) AS total_veiculos,
        CAST(SUM(fato.mortos) AS BIGINT) AS total_mortos,
        CAST(SUM(fato.feridos) AS BIGINT) AS total_feridos,
        CAST(SUM(fato.feridos_graves) AS BIGINT) AS total_feridos_graves,
        CAST(SUM(fato.feridos_leves) AS BIGINT) AS total_feridos_leves,
        CAST(SUM(fato.ilesos) AS BIGINT) AS total_ilesos,
        ROUND(CAST(SUM(fato.mortos) AS DOUBLE) / NULLIF(COUNT(fato.id), 0) * 100, 2) AS pct_mortalidade
    FROM
        "gold"."stg" AS fato
        JOIN temp_dim_localizacao AS localizacao ON fato.sk_localizacao = localizacao.id
        JOIN temp_dim_condicao_metereologica AS condicao_metereologica ON fato.sk_condicao_metereologica = condicao_metereologica.id
        JOIN temp_dim_tempo AS tempo ON fato.sk_tempo = tempo.id
        JOIN temp_dim_causa AS causa ON fato.sk_causa = causa.id
        JOIN temp_dim_tipo AS tipo ON fato.sk_tipo = tipo.id
        JOIN temp_dim_classificacao AS classificacao ON fato.sk_classificacao = classificacao.id
        
    GROUP BY
        localizacao.uf,
        localizacao.municipio,

        condicao_metereologica.condicao,
        tempo.mes,
        tempo.fase_dia,

        causa.causa,
        tipo.tipo,
        classificacao.classificacao
);

MERGE INTO "gold"."agg_letalidade_clima_tempo" AS target 
USING temp_agg_letalidade_clima_tempo AS source 
    ON target.id = source.id

WHEN MATCHED THEN
UPDATE SET
    total_ocorrencias = source.total_ocorrencias,
    total_pessoas = source.total_pessoas,
    total_veiculos = source.total_veiculos,
    total_mortos = source.total_mortos,
    total_feridos = source.total_feridos,
    total_feridos_graves = source.total_feridos_graves,
    total_feridos_leves = source.total_feridos_leves,
    total_ilesos = source.total_ilesos,
    pct_mortalidade = source.pct_mortalidade

WHEN NOT MATCHED THEN 
INSERT (
    id,

    uf, 
    municipio,

    condicao_metereologica,
    mes,
    fase_dia,

    causa_acidente,
    tipo_acidente,
    classificacao_acidente,

    total_ocorrencias,
    total_pessoas,
    total_veiculos,
    total_mortos,
    total_feridos,
    total_feridos_graves,
    total_feridos_leves,
    total_ilesos,
    pct_mortalidade
) 
VALUES (
    source.id,

    source.uf, 
    source.municipio,

    source.condicao_metereologica,
    source.mes,
    source.fase_dia,

    source.causa_acidente,
    source.tipo_acidente,
    source.classificacao_acidente,

    source.total_ocorrencias,
    source.total_pessoas,
    source.total_veiculos,
    source.total_mortos,
    source.total_feridos,
    source.total_feridos_graves,
    source.total_feridos_leves,
    source.total_ilesos,
    source.pct_mortalidade
);

DROP TABLE IF EXISTS temp_dim_localizacao;
DROP TABLE IF EXISTS temp_dim_pista;
DROP TABLE IF EXISTS temp_dim_condicao_metereologica;
DROP TABLE IF EXISTS temp_dim_causa;
DROP TABLE IF EXISTS temp_dim_tipo;
DROP TABLE IF EXISTS temp_dim_classificacao;

DROP TABLE IF EXISTS temp_agg_letalidade_clima_tempo;