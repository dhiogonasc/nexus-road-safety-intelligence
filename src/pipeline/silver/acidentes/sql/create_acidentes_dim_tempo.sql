CREATE
OR REPLACE TABLE "acidentes"."dim_tempo" AS WITH base_tempo AS (
    SELECT
        DISTINCT LOWER(
            REGEXP_REPLACE(
                strip_accents(
                    TRIM(COALESCE(dia_semana :: VARCHAR, 'nao_informado'))
                ),
                '[^a-zA-Z0-9]+',
                '_',
                'g'
            )
        ) AS dia_semana,
        LOWER(
            REGEXP_REPLACE(
                strip_accents(
                    TRIM(COALESCE(fase_dia :: VARCHAR, 'nao_informado'))
                ),
                '[^a-zA-Z0-9]+',
                '_',
                'g'
            )
        ) AS fase_dia,
        TRY_CAST(data_inversa AS DATE) AS base_data,
        TRY_CAST(horario AS TIME) AS base_hora
    FROM
        "acidentes"."stg_ocorrencias"
    WHERE
        data_inversa IS NOT NULL
        AND horario IS NOT NULL
),
formatted_tempo AS (
    SELECT
        dia_semana,
        fase_dia,
        (base_data + base_hora) AS data_hora,
        EXTRACT(
            YEAR
            FROM
                base_data
        ) AS ano,
        EXTRACT(
            MONTH
            FROM
                base_data
        ) AS mes,
        EXTRACT(
            DAY
            FROM
                base_data
        ) AS dia,
        EXTRACT(
            HOUR
            FROM
                base_hora
        ) AS hora
    FROM
        base_tempo
),
ref_tempo AS (
    SELECT
        *,
        md5(
            concat_ws(
                '_',
                COALESCE(data_hora :: VARCHAR, ''),
                COALESCE(dia_semana, ''),
                COALESCE(fase_dia, '')
            )
        ) AS id
    FROM
        formatted_tempo
)
SELECT
    id,
    data_hora,
    ano,
    mes,
    dia,
    hora,
    dia_semana,
    fase_dia
FROM
    ref_tempo;