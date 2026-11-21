{{
    config(
        materialized='incremental',
        unique_key='sk_local'
    )
}}

with

staging as (
    select distinct
        br,
        zona,
        regiao,
        estado
    from {{ ref('stg_ocorrencias') }}
),

dimension as (
    select
        md5(
            br      || '-' || 
            regiao  || '-' || 
            estado  || '-' || 
            zona
        ) as sk_local, *
    from staging
)

select * from dimension

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} as this
        where this.sk_local = dimension.sk_local
    )
{% endif %}
