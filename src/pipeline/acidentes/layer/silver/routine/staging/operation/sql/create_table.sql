CREATE OR REPLACE MACRO normalize_value(str) AS 
    CASE 
        WHEN str IS NULL OR TRIM(str :: VARCHAR) = '' THEN 'não informado'
        ELSE 
            REGEXP_REPLACE(
            REGEXP_REPLACE(
                LOWER(TRIM(str :: VARCHAR)), 
                '[\s\-_/,]+', ' ', 'g'
            ), 
                '[^\p{L}\p{N}\s]', '', 'g'
            )
    END;

CREATE OR REPLACE TABLE "silver"."stg" AS
WITH 
ultima_carga AS (
    SELECT * 
    FROM read_parquet('{storage_path}/**/*.parquet', hive_partitioning = true)
    WHERE data_carga = (
        SELECT MAX(data_carga) 
        FROM read_parquet('{log_path}/**/*.parquet')
    )
),
base_tempo AS (
    SELECT 
        *,
        TRY_CAST(data_inversa AS DATE) AS data,
        TRY_CAST(horario AS TIME) AS horario
    FROM ultima_carga
)
SELECT 
    COALESCE(id :: VARCHAR, 'não informado') AS id_ocorrencia,

    -- dim_tempo
    (data + horario) AS data_hora,
    EXTRACT(YEAR FROM data) AS ano,
    EXTRACT(MONTH FROM data) AS mes,
    EXTRACT(DAY FROM data) AS dia,
    EXTRACT(HOUR FROM horario) AS hora,
    normalize_value(dia_semana) AS dia_semana,
    normalize_value(fase_dia) AS fase_dia,

    -- dim_local
    normalize_value(uf) AS uf,
    normalize_value(br) AS br,
    TRY_CAST(REPLACE(km :: VARCHAR, ',', '.') AS DOUBLE) AS km,
    normalize_value(sentido_via) AS sentido_via,
    normalize_value(municipio) AS municipio,
    CASE 
        WHEN normalize_value(uso_solo) = 'não' THEN 'rural'
        WHEN normalize_value(uso_solo) = 'sim' THEN 'urbano'
    END AS uso_solo,
    TRY_CAST(REPLACE(latitude :: VARCHAR, ',', '.') AS DOUBLE) AS latitude,
    TRY_CAST(REPLACE(longitude :: VARCHAR, ',', '.') AS DOUBLE) AS longitude,
    
    -- dim_pista
    COALESCE(tracado_via :: VARCHAR, 'não informado') AS tracado_via,
    COALESCE(tipo_pista :: VARCHAR, 'não informado') AS tipo_pista,

    -- dim_jurisdicao
    TRIM(COALESCE(UPPER(uop :: VARCHAR), 'não informado')) AS uop,
    normalize_value(regional) AS regional,
    normalize_value(delegacia) AS delegacia,

    -- dim_categoria
    normalize_value(causa_acidente) AS causa_acidente,
    normalize_value(tipo_acidente) AS tipo_acidente,
    normalize_value(classificacao_acidente) AS classificacao_acidente,
    
    -- dim_clima
    normalize_value(condicao_metereologica) AS condicao_metereologica,
    
    -- payload
    COALESCE(TRY_CAST(pessoas AS INTEGER), 0) AS pessoas,
    COALESCE(TRY_CAST(mortos AS INTEGER), 0) AS mortos,
    COALESCE(TRY_CAST(feridos_leves AS INTEGER), 0) AS feridos_leves,
    COALESCE(TRY_CAST(feridos_graves AS INTEGER), 0) AS feridos_graves,
    COALESCE(TRY_CAST(feridos AS INTEGER), 0) AS feridos,
    COALESCE(TRY_CAST(ilesos AS INTEGER), 0) AS ilesos,
    COALESCE(TRY_CAST(ignorados AS INTEGER), 0) AS ignorados,
    COALESCE(TRY_CAST(veiculos AS INTEGER), 0) AS veiculos
FROM base_tempo;