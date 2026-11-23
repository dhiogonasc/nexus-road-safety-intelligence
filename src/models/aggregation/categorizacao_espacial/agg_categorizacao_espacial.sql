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

        cast(
            round(sum(total_mortos)::decimal / nullif(sum(total_envolvidos), 0), 2) 
            as decimal(5, 2)
        ) as taxa_mortalidade,
        cast(
            round(sum(total_mortos)::decimal / nullif(count(id), 0), 2)
            as decimal(5, 2)
        ) as indice_mortalidade_ocorrencia,
        cast(
            round(sum(total_envolvidos)::decimal / nullif(count(id), 0), 2)
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
            staging.sk_local || '-' || 
            staging.sk_categoria
        ) as id,

        local.br,
        local.regiao,
        local.estado,
        local.tipo_area,

        categoria.classificacao_acidente,
        
        staging.total_ocorrencias,
        staging.taxa_mortalidade,
        staging.indice_mortalidade_ocorrencia,
        staging.indice_envolvimento_ocorrencia
    from staging

    join {{ ref('dim_local') }} as local
        on staging.sk_local = local.sk_local

    join {{ ref('dim_categoria') }} as categoria
        on staging.sk_categoria = categoria.sk_categoria
)

select * from aggregation

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} as this
        where this.id = aggregation.id
    )
{% endif %}