CREATE OR REPLACE TABLE "silver"."stg" AS 
WITH 
last_charge AS (
    SELECT *
    FROM read_parquet(
        '{storage_path}/**/*.parquet', 
        hive_partitioning = true
    )
    WHERE data_carga = (
        SELECT MAX(data_carga) 
        FROM read_parquet(
            '{log_path}/**/*.parquet'
        )
    )
),
parsed_base AS (
    SELECT 
        *,
        TRY_CAST(data_inversa AS DATE) AS dt_parsed,
        TRY_CAST(horario AS TIME) AS hr_parsed
    FROM last_charge
)
SELECT 
    COALESCE(id :: VARCHAR, 'nao_informado') AS id_ocorrencia,
    COALESCE(dia_semana :: VARCHAR, 'nao_informado') AS dia_semana,
    COALESCE(fase_dia :: VARCHAR, 'nao_informado') AS fase_dia,
    
    (dt_parsed + hr_parsed) AS data_hora,
    EXTRACT(YEAR FROM dt_parsed) AS ano,
    EXTRACT(MONTH FROM dt_parsed) AS mes,
    EXTRACT(DAY FROM dt_parsed) AS dia,
    EXTRACT(HOUR FROM hr_parsed) AS hora,

    TRIM(COALESCE(uf :: VARCHAR, 'nao_informado')) AS uf,
    TRIM(COALESCE(br :: VARCHAR, 'nao_informado')) AS br,
    TRY_CAST(REPLACE(km :: VARCHAR, ',', '.') AS DOUBLE) AS km,
    TRIM(COALESCE(municipio :: VARCHAR, 'nao_informado')) AS municipio,
    TRIM(COALESCE(regional :: VARCHAR, 'nao_informado')) AS regional,
    TRIM(COALESCE(delegacia :: VARCHAR, 'nao_informado')) AS delegacia,
    TRIM(COALESCE(uop :: VARCHAR, 'nao_informado')) AS uop,

    TRY_CAST(REPLACE(latitude :: VARCHAR, ',', '.') AS DOUBLE) AS latitude,
    TRY_CAST(REPLACE(longitude :: VARCHAR, ',', '.') AS DOUBLE) AS longitude,

    COALESCE(causa_acidente :: VARCHAR, 'nao_informado') AS causa_acidente,
    COALESCE(tipo_acidente :: VARCHAR, 'nao_informado') AS tipo_acidente,
    COALESCE(classificacao_acidente :: VARCHAR, 'nao_informado') AS classificacao_acidente,
    COALESCE(condicao_metereologica :: VARCHAR, 'nao_informado') AS condicao_metereologica,
    COALESCE(sentido_via :: VARCHAR, 'nao_informado') AS sentido_via,
    COALESCE(tracado_via :: VARCHAR, 'nao_informado') AS tracado_via,
    COALESCE(tipo_pista :: VARCHAR, 'nao_informado') AS tipo_pista,
    COALESCE(uso_solo :: VARCHAR, 'nao_informado') AS uso_solo,
    
    COALESCE(pessoas, 0) AS pessoas,
    COALESCE(mortos, 0) AS mortos,
    COALESCE(feridos_leves, 0) AS feridos_leves,
    COALESCE(feridos_graves, 0) AS feridos_graves,
    COALESCE(feridos, 0) AS feridos,
    COALESCE(ilesos, 0) AS ilesos,
    COALESCE(ignorados, 0) AS ignorados,
    COALESCE(veiculos, 0) AS veiculos
FROM parsed_base;