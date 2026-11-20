{{ config(materialized='table') }}

with source_data as (
    select * 
    from read_csv_auto(
        '{{ var("raw_ocorrencias_csv_path") }}', 
        header = true, 
        delim = ';', 
        encoding='ISO-8859-1',
        all_varchar=true
    )
),

normalized as (
    select
        try_cast(id as bigint) as id_ocorrencia,
        
        {{ normalize_txt_value('tipo_acidente') }} as tipo_acidente,
        {{ normalize_txt_value('causa_acidente') }} as causa_acidente,
        {{ normalize_txt_value('classificacao_acidente') }} as classificacao_acidente,

        {{ normalize_txt_value('condicao_metereologica') }} as condicao_metereologica,

        try_cast(coalesce(br, '0') as integer) as br,
        try_cast(coalesce(replace(cast(km as varchar), ',', '.'), '0') as decimal(13, 3)) as km,
        {{ normalize_txt_value('sentido_via') }} as sentido,
        {{ normalize_txt_value('uf') }} as uf_sigla,
        {{ transcript_uf_sail('uf') }} as uf_nome,
        {{ normalize_txt_value('municipio') }} as municipio,
        {{ classify_area_type('uso_solo') }} as tipo_area,

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
    from source_data
)

select * from normalized