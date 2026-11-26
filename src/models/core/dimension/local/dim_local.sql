{{
    config(
        materialized='incremental',
        unique_key='sk_local'
    )
}}

with

malha_geografica as ( 
    select * from {{ ref('base_malha_geografica') }}
),

staging as (
    select distinct uf, br, tipo_area
    from {{ ref('stg_ocorrencias') }}
    where 1=1
        and uf <> 'não informado'
        and br <> 'não informado'
        and tipo_area <> 'não informado'
),

enriched as (
    select
        malha_geografica.regiao,
        malha_geografica.estado,
        staging.uf,
        staging.br,
        staging.tipo_area
    from staging
    left join malha_geografica
        on staging.uf = malha_geografica.uf 
),

dimension as (
    select
        md5(
            uf || '-' || 
            br || '-' || 
            tipo_area
        ) as sk_local, 
        enriched.uf,
        enriched.br,
        enriched.regiao,
        enriched.estado,
        enriched.tipo_area
    from enriched
)

select * from dimension

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} as this
        where this.sk_local = dimension.sk_local
    )
{% endif %}
