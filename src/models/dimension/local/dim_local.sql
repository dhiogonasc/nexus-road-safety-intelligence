{{
    config(
        materialized='incremental',
        unique_key='sk_local'
    )
}}

with dimension as (
    select distinct
        md5(
            cast(br as varchar) || '-' || 
            cast(km as varchar) || '-' || 
            sentido             || '-' ||
            uf_sigla            || '-' || 
            municipio           || '-' || 
            tipo_area
        ) as sk_local,
        br,
        km,
        sentido,
        uf_sigla,
        uf_nome,
        municipio,
        tipo_area
    from {{ ref('stg_ocorrencias') }}
)

select * from dimension

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} 
        where {{ this }}.sk_local = dimension.sk_local
    )
{% endif %}