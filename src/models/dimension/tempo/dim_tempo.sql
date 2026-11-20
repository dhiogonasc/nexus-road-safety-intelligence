{{
    config(
        materialized='incremental',
        unique_key='sk_tempo'
    )
}}

with dimension as (
    select distinct
        md5(cast(data as varchar) || '-' || fase_dia) as sk_tempo,
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
    where data is not null
)

select * from dimension

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} 
        where {{ this }}.sk_tempo = dimension.sk_tempo
    )
{% endif %}