{{ config(materialized='table') }}

with raw as (
    select * 
    from read_csv_auto(
        '{{ var("raw_ocorrencias_csv_path") }}', 
        delim = ';', 
        encoding='ISO-8859-1',
        header = true, 
        all_varchar=true,
        union_by_name=true,
    )
),

base_malha_geografica as ( 
    select * from {{ ref('base_malha_geografica') }}
),

normalized_time as (
    select
        coalesce(
            try_strptime(data_inversa, '%d/%m/%Y'),
            try_strptime(data_inversa, '%Y-%m-%d'),
            try_cast(data_inversa as date)
        ) as data,
        * exclude (data_inversa)
    from raw
),

staging as (
    select
        try_cast(id as bigint) as id_ocorrencia,
        
        {{ normalize_txt_value('tipo_acidente') }} as tipo_acidente,
        {{ normalize_txt_value('causa_acidente') }} as causa_acidente,
        {{ normalize_txt_value('classificacao_acidente') }} as classificacao_acidente,

        {{ normalize_txt_value('condicao_metereologica') }} as condicao_metereologica,

        {{ normalize_txt_value('br') }} as br,
        {{ normalize_txt_value('uf') }} as uf,
        {{ classify_zone('uso_solo') }} as zona,

        cast(data as date) as data,
        try_cast(extract(year from data) as integer) as ano,
        try_cast(extract(month from data) as integer) as mes,
        try_cast(extract(week from data) as integer ) as semana,
        try_cast(isodow(data) as integer ) as dia_semana,
        try_cast({{ enumerate_day_period('fase_dia') }} as integer ) as fase_dia,
        
        {{ transcript_month_number("extract(month from data)") }} as mes_nome,
        {{ transcript_weekday_number("isodow(data)") }} as dia_semana_nome,
        {{ normalize_txt_value('fase_dia') }} as fase_dia_desc,
        
        try_cast(coalesce(pessoas, '0') as integer) as total_envolvidos,
        try_cast(coalesce(ilesos, '0') as integer) as total_ilesos,
        try_cast(coalesce(mortos, '0') as integer) as total_mortos,
        try_cast(coalesce(feridos, '0') as integer) as total_feridos
    from normalized_time
),

enriched_staging as (
    select 
        staging.* exclude(uf),
        malha.regiao,
        malha.estado
    from staging as staging
    
    left join base_malha_geografica as malha 
        on staging.uf = malha.uf

    qualify row_number() over (
        partition by id_ocorrencia
        order by 
            total_mortos desc, 
            total_envolvidos desc
    ) = 1
)

select * from enriched_staging