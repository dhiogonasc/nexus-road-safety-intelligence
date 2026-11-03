CREATE OR REPLACE MACRO normalize_value(str) AS 
    CASE 
        WHEN str IS NULL OR TRIM(str :: VARCHAR) = '' THEN 'não informado'
        ELSE 
            REGEXP_REPLACE(
            REGEXP_REPLACE(
                LOWER(TRIM(str :: VARCHAR)), 
                '[\s\-_/,]+', ' ', 'g'
            ), 
                '[^\p{{L}}\p{{N}}\s]', '', 'g'
            )
    END;

CREATE OR REPLACE TABLE "silver"."stg_ocorrencias" AS
WITH 
ultima_carga AS (
    SELECT * 
    FROM read_parquet('{source_storage_path}/**/*.parquet', hive_partitioning = true)
    WHERE data_carga = (
        SELECT * 
        FROM read_parquet('{source_log_path}/**/*.parquet')
    )
),
SELECT 
    COALESCE(id :: VARCHAR, 'não informado') AS id_ocorrencia,

    -- dim_tempo
    EXTRACT(YEAR FROM TRY_CAST(data_inversa AS DATE)) AS ano,
    EXTRACT(MONTH FROM TRY_CAST(data_inversa AS DATE)) AS mes,
    EXTRACT(WEEK FROM TRY_CAST(data_inversa AS DATE)) AS semana,
    normalize_value(dia_semana) AS dia_semana,
    normalize_value(fase_dia) AS fase_dia,

    -- dim_local
    normalize_value(uf) AS uf,
    normalize_value(br) AS br,
    TRY_CAST(REPLACE(km :: VARCHAR, ',', '.') AS DOUBLE) AS km,
    normalize_value(sentido_via) AS sentido,
    normalize_value(municipio) AS municipio,
    CASE 
        WHEN normalize_value(uso_solo) = 'não' THEN 'rural'
        WHEN normalize_value(uso_solo) = 'sim' THEN 'urbano'
        ELSE 'não informado'
    END AS tipo_area,

    -- dim_clima
    normalize_value(condicao_metereologica) AS condicao_metereologica,
    
    -- dim_categoria
    normalize_value(causa_acidente) AS causa,
    normalize_value(tipo_acidente) AS tipo,
    normalize_value(classificacao_acidente) AS classificacao,
    
    
    -- payload
    COALESCE(TRY_CAST(pessoas AS INTEGER), 0) AS pessoas,
    COALESCE(TRY_CAST(mortos AS INTEGER), 0) AS mortos,
    COALESCE(TRY_CAST(feridos_leves AS INTEGER), 0) AS feridos_leves,
    COALESCE(TRY_CAST(feridos_graves AS INTEGER), 0) AS feridos_graves,
    COALESCE(TRY_CAST(feridos AS INTEGER), 0) AS feridos,
    COALESCE(TRY_CAST(ilesos AS INTEGER), 0) AS ilesos,
    COALESCE(TRY_CAST(ignorados AS INTEGER), 0) AS ignorados,
    COALESCE(TRY_CAST(veiculos AS INTEGER), 0) AS veiculos
FROM ultima_carga;