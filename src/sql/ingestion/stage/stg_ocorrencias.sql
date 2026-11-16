CREATE OR REPLACE MACRO normalize_value(str) AS  
    CASE  
        WHEN str 
            IS NULL 
            OR LOWER(TRIM(str :: VARCHAR)) IN ('na', 'n/a', 'nan', 'null', 'none', '-', '') 
                THEN 'não informado'
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
SELECT 
    TRY_CAST(id AS BIGINT) AS id_ocorrencia,

    -- dim_tempo
    EXTRACT(YEAR FROM TRY_CAST(data_inversa AS DATE)) AS ano,
    EXTRACT(MONTH FROM TRY_CAST(data_inversa AS DATE)) AS mes,
    EXTRACT(WEEK FROM TRY_CAST(data_inversa AS DATE)) AS semana,
    ISODOW(TRY_CAST(data_inversa AS DATE)) AS dia_semana,
    CASE (normalize_value(fase_dia))
        WHEN 'amanhecer' THEN 1
        WHEN 'pleno dia' THEN 2
        WHEN 'anoitecer' THEN 3
        WHEN 'plena noite' THEN 4
        ELSE 5
    END AS fase_dia,

        -- coluna auxiliar de exibição
    normalize_value(STRFTIME(TRY_CAST(data_inversa AS DATE), '%B')) AS mes_str,
    normalize_value(STRFTIME(TRY_CAST(data_inversa AS DATE), '%A')) AS dia_semana_str,
    normalize_value(fase_dia) AS fase_dia_str,

    -- dim_local
    normalize_value(uf) AS uf,
    COALESCE(TRY_CAST(br AS INTEGER), 0) AS br,
    COALESCE(TRY_CAST(REPLACE(km :: VARCHAR, ',', '.') AS DECIMAL(5, 3)), 0) AS km,
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
FROM (
    SELECT * 
    FROM read_parquet('{raw_ocorrencias_storage_path}/**/*.parquet', hive_partitioning = true)
    WHERE data_carga = (
        SELECT * 
        FROM read_parquet('{raw_ocorrencias_log_path}/**/*.parquet')
    )
);