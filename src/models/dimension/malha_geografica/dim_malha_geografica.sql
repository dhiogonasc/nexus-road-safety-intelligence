{{
    config(
        materialized='incremental',
        unique_key='sk_malha_geografica'
    )
}}

with

malha_geografica as ( 
    select * from {{ ref('base_malha_geografica') }}
),

staging as (
    select distinct
        uf,
        tipo_area
    from {{ ref('stg_ocorrencias') }}
),

enriched as (
    select
        malha_geografica.regiao,
        malha_geografica.estado,
        staging.*
    from staging
    left join malha_geografica
        on staging.uf = malha_geografica.uf 
),

dimension as (
    select
        md5(
            uf || '-' || 
            tipo_area
        ) as sk_malha_geografica, 
        * exclude(uf)
    from enriched
)

select * from dimension

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} as this
        where this.sk_malha_geografica = dimension.sk_malha_geografica
    )
{% endif %}
