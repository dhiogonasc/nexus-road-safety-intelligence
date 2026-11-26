{{
    config(
        materialized='incremental',
        unique_key='sk_clima'
    )
}}

with 

staging as (
    select distinct condicao_metereologica
    from {{ ref('stg_ocorrencias') }}
    where 1=1
        and (
            condicao_metereologica <> 'não informado'
            or condicao_metereologica <> 'ignorado'
        )
),

dimension as (
    select md5(condicao_metereologica) as sk_clima, *
    from staging
)

select * from dimension

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} as this
        where this.sk_clima = dimension.sk_clima
    )
{% endif %}