{{
    config(
        materialized='incremental',
        unique_key='sk_categoria'
    )
}}

with dimension as (
    select distinct

        md5(
            tipo_acidente   || '-' || 
            causa_acidente  || '-' || 
            classificacao_acidente
        ) as sk_categoria,

        tipo_acidente,
        causa_acidente,
        classificacao_acidente

    from {{ ref('stg_ocorrencias') }}
)

select * from dimension

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} 
        where {{ this }}.sk_categoria = dimension.sk_categoria
    )
{% endif %}