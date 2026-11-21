{{ config(materialized='table') }}

with base_ocorrencias as (
    select * 
    from read_csv_auto(
        '{{ var("raw_ocorrencias_csv_path") }}', 
        header = true, 
        delim = ';', 
        encoding='ISO-8859-1',
        all_varchar=true
    )
),

normalized_ocorrencias as (
    select
        try_cast(id as bigint) as id_ocorrencia,
        
        {{ normalize_txt_value('tipo_acidente') }} as tipo_acidente,
        {{ normalize_txt_value('causa_acidente') }} as causa_acidente,
        {{ normalize_txt_value('classificacao_acidente') }} as classificacao_acidente,

        {{ normalize_txt_value('condicao_metereologica') }} as condicao_metereologica,

        try_cast(coalesce(br, '0') as integer) as br,
        {{ classify_zone('uso_solo') }} as zona,
        {{ normalize_txt_value('uf') }} as uf,

        try_cast(data_inversa as date) as data,
        try_cast(extract(year from try_cast(data_inversa as date)) as integer) as ano,
        try_cast(extract(month from try_cast(data_inversa as date)) as integer) as mes,
        try_cast(extract(week from try_cast(data_inversa as date)) as integer ) as semana,
        try_cast(isodow(try_cast(data_inversa as date)) as integer ) as dia_semana,
        try_cast({{ enumerate_day_period('fase_dia') }} as integer ) as fase_dia,
        {{ transcript_month_number("extract(month from try_cast(data_inversa as date))") }} as mes_nome,
        {{ transcript_weekday_number("isodow(try_cast(data_inversa as date))") }} as dia_semana_nome,
        {{ normalize_txt_value('fase_dia') }} as fase_dia_desc,
        
        try_cast(coalesce(veiculos, '0') as integer) as total_veiculos,
        try_cast(coalesce(pessoas, '0') as integer) as total_envolvidos,
        try_cast(coalesce(mortos, '0') as integer) as total_mortos,
        try_cast(coalesce(feridos, '0') as integer) as total_feridos,
        try_cast(coalesce(ilesos, '0') as integer) as total_ilesos
    from base_ocorrencias
),

malha as (
    select * from {{ ref('base_malha_geografica') }}
),

staging as (
    select 
        ocorrencias.* exclude(uf),
        malha.regiao,
        malha.estado
    from normalized_ocorrencias as ocorrencias
    join malha on ocorrencias.uf = malha.uf
)

select * from staging