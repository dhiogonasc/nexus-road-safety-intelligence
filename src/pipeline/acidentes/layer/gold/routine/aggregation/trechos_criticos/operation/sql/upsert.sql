CREATE TEMP TABLE temp_dim_tempo AS SELECT *
FROM read_parquet('{silver_storage_path["dim_tempo"]}') ;

CREATE TEMP TABLE temp_dim_condicao_metereologica AS SELECT *
FROM read_parquet('{silver_storage_path["dim_condicao_metereologica"]}') ;

CREATE TEMP TABLE temp_dim_pista AS SELECT *
FROM read_parquet('{silver_storage_path["dim_pista"]}') ;

SELECT setval(
    'seq_condicoes_via', 
    GREATEST(COALESCE((SELECT MAX(id) FROM "gold"."condicoes_via"), 0), 1)
);

CREATE TEMP TABLE temp_condicoes_via AS
SELECT nextval('seq_condicoes_via') AS id, *
FROM (
    SELECT
        tempo.ano,
        tempo.mes,
        tempo.dia,
        tempo.dia_semana,
        tempo.fase_dia,

        cm.condicao AS condicao_metereologica,

        pista.sentido AS sentido_via,
        pista.tracado AS tracado_via,
        pista.tipo AS tipo_via,
        pista.solo AS solo_via,

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
        "gold"."ft_staging" AS fato
        JOIN temp_dim_tempo AS tempo ON fato.sk_tempo = tempo.id
        JOIN temp_dim_condicao_metereologica AS cm ON fato.sk_condicao_metereologica = cm.id
        JOIN temp_dim_pista AS pista ON fato.sk_pista = pista.id
    GROUP BY
        tempo.ano,
        tempo.mes,
        tempo.dia,
        tempo.dia_semana,
        tempo.fase_dia,

        cm.condicao,

        pista.sentido,
        pista.tracado,
        pista.tipo,
        pista.solo
) AS source_data;

MERGE INTO "gold"."condicoes_via" AS target 
USING temp_condicoes_via AS source 
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
    ano,
    mes,
    dia,
    dia_semana,
    fase_dia,
    condicao_metereologica,
    sentido_via,
    tracado_via,
    tipo_via,
    solo_via,
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
    source.ano,
    source.mes,
    source.dia,
    source.dia_semana,
    source.fase_dia,
    source.condicao_metereologica,
    source.sentido_via,
    source.tracado_via,
    source.tipo_via,
    source.solo_via,
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

DROP TABLE IF EXISTS temp_dim_tempo;
DROP TABLE IF EXISTS temp_dim_condicao_metereologica;
DROP TABLE IF EXISTS temp_dim_pista;

DROP TABLE IF EXISTS temp_condicoes_via;