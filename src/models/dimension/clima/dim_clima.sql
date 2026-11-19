{{
    config(
        materialized='incremental',
        unique_key='sk_clima'
    )
}}

with dimension as (
    select distinct
        md5(condicao_metereologica) as sk_clima,
        condicao_metereologica
    from {{ ref('stg_ocorrencias') }}
)

select * from dimension

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} 
        where {{ this }}.sk_clima = dimension.sk_clima
    )
{% endif %}