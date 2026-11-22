{{
    config(
        materialized='incremental',
        unique_key='sk_tempo'
    )
}}

with 

staging as (
    select distinct
        data,
        fase_dia
    from {{ ref('stg_ocorrencias') }}
),

extraction as (
    select
        data,
        cast(extract(year from data) as integer) as ano,
        cast(extract(month from data) as integer) as mes,
        cast(extract(week from data) as integer ) as semana,
        cast(isodow(data) as integer ) as dia_semana,
        cast({{ enumerate_day_period('fase_dia') }} as integer ) as fase_dia,
        fase_dia as fase_dia_nome
    from staging
),

description as (
    select *,
        {{ transcript_month_number('data') }} as mes_nome,
        {{ transcript_weekday_number('data') }} as dia_semana_nome
    from extraction
),

dimension as (
    select
        md5(
            cast(data as varchar) || '-' || 
            fase_dia
        ) as sk_tempo, *
    from description
)

select * from dimension

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} as this
        where this.sk_tempo = dimension.sk_tempo
    )
{% endif %}
