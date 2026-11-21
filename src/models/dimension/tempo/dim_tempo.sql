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
        ano,
        mes,
        semana,
        dia_semana,
        fase_dia,
        mes_nome,
        dia_semana_nome,
        fase_dia_desc
    from {{ ref('stg_ocorrencias') }}
),

dimension as (
    select
        md5(
            cast(data as varchar) || '-' || 
            fase_dia
        ) as sk_tempo, *
    from staging
)

select * from dimension

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} as this
        where this.sk_tempo = dimension.sk_tempo
    )
{% endif %}
