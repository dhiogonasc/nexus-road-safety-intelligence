{{ config(materialized='table') }}

with source_data as (
    select * 
    from read_csv_auto(
        '{{ var("raw_ocorrencias_csv_path") }}', 
        header = true, 
        delim = ';', 
        encoding = 'latin1'
    )
),

normalized as (
    select
        try_cast(id as bigint) as id_ocorrencia,

        -- dim_tempo
        try_cast(data_inversa as date) as data,
        extract(year from try_cast(data_inversa as date)) as ano,
        extract(month from try_cast(data_inversa as date)) as mes,
        extract(week from try_cast(data_inversa as date)) as semana,
        isodow(try_cast(data_inversa as date)) as dia_semana,
        {{ classify_day_period('fase_dia') }}as fase_dia,
        {{ transcript_month_number("extract(month from try_cast(data_inversa as date))") }} as mes_txt,
        {{ transcript_weekday_number("isodow(try_cast(data_inversa as date))") }} as dia_semana_txt,
        {{ normalize_txt_value('fase_dia') }} as fase_dia_txt,

        -- dim_local
        coalesce(try_cast(br as integer), 0) as br,
        coalesce(try_cast(replace(cast(km as varchar), ',', '.') as decimal(5, 3)), 0) as km,
        {{ normalize_txt_value('sentido_via') }} as sentido,
        {{ normalize_txt_value('uf') }} as uf_sigla,
        {{ transcript_uf_sail('uf') }} as uf_nome,
        {{ normalize_txt_value('municipio') }} as municipio,
        {{ classify_area_type('uso_solo') }}as tipo_area,

        -- dim_clima
        {{ normalize_txt_value('condicao_metereologica') }} as condicao_metereologica,
        
        -- dim_categoria
        {{ normalize_txt_value('tipo_acidente') }} as tipo_acidente,
        {{ normalize_txt_value('causa_acidente') }} as causa_acidente,
        {{ normalize_txt_value('classificacao_acidente') }} as classificacao_acidente,
        
        -- metrics
        coalesce(try_cast(veiculos as integer), 0) as total_veiculos_envolvidos,
        coalesce(try_cast(pessoas as integer), 0) as total_pessoas_envolvidas,
        coalesce(try_cast(mortos as integer), 0) as total_mortos,
        coalesce(try_cast(feridos as integer), 0) as total_feridos,
        coalesce(try_cast(ilesos as integer), 0) as total_ilesos
    from source_data
)

select * from normalized