{{
    config(
        materialized='incremental',
        unique_key='sk_malha_rodoviaria'
    )
}}

with

staging as (
    select distinct
        br,
        km,
        sentido_via,
        tipo_pista
    from {{ ref('stg_ocorrencias') }}
),

dimension as (
    select
        md5(
            br                  || '-' ||
            cast(km as varchar) || '-' ||
            tracado_via         || '-' ||
            tipo_pista
        ) as sk_malha_rodoviaria, *
    from staging
)

select * from dimension

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} as this
        where this.sk_malha_rodoviaria = dimension.sk_malha_rodoviaria
    )
{% endif %}
