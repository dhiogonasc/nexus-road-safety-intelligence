{{
    config(
        materialized='incremental',
        unique_key='id',    
    )
}}

with 

staging as (
    select distinct
        sk_local,
        sk_categoria,

        cast(count(id) as bigint) as total_ocorrencias,
        cast(sum(total_mortos) as bigint) as total_mortos,
        cast(sum(total_envolvidos) as bigint) as total_envolvidos,

        cast(
            round(sum(total_mortos)/ nullif(sum(total_envolvidos), 0), 2) 
            as decimal(5, 2)
        ) as taxa_mortalidade,
        cast(
            round(sum(total_mortos) / nullif(count(id), 0), 2)
            as decimal(5, 2)
        ) as indice_mortalidade_ocorrencia,
        cast(
            round(sum(total_envolvidos) / nullif(count(id), 0), 2)
            as decimal(5, 2)
        ) as indice_envolvimento_ocorrencia

    from {{ ref('fct_ocorrencia') }} fato

    group by
        sk_local,
        sk_categoria
),

aggregation as (
    select
        md5(
            cast(staging.sk_local as varchar) || '-' || 
            cast(staging.sk_categoria as varchar)
        ) as id,

        local.br,
        local.regiao,
        local.estado,
        local.zona,

        categoria.tipo_acidente,
        categoria.causa_acidente,
        categoria.classificacao_acidente,

        staging.total_envolvidos,
        staging.total_mortos,
        staging.total_ocorrencias,
        staging.taxa_mortalidade,
        staging.indice_mortalidade_ocorrencia,
        staging.indice_envolvimento_ocorrencia
    from staging

    inner join {{ ref('dim_local') }} as local
        on staging.sk_local = local.sk_local

    inner join {{ ref('dim_categoria') }} as categoria
        on staging.sk_categoria = categoria.sk_categoria
)

select * from aggregation

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} as this
        where this.id = aggregation.id
    )
{% endif %}