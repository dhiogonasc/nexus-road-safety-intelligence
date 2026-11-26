{{
    config(
        materialized='incremental',
        unique_key='sk_categoria',
    )
}}

with 

staging as (
    select distinct classificacao_acidente
    from {{ ref('stg_ocorrencias') }}
),

dimension as (
    select md5(classificacao_acidente) as sk_categoria, *
    from staging
)

select * from dimension

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} as this
        where this.sk_categoria = dimension.sk_categoria
    )
{% endif %}