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
    select distinct 
        uf, 
        case
            when br = 'não informado' then 'não informado'
            else 'br-' || lpad(regexp_replace(br, '[^\d]', '', 'g'), 3, '0')
        end as br,
        case 
            when tipo_area in ('não', 'rural') then 'rural'
            when tipo_area in ('sim', 'urbano') then 'urbano'
            else 'não informado'
        end as tipo_area
    from {{ ref('stg_ocorrencias') }}
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
