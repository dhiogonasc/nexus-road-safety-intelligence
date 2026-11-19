{{
    config(
        materialized='incremental',
        unique_key='id'
    )
}}

with aggregation as (

    select
        md5(
            cast(local.br as varchar)   || '-' ||
            cast(local.km as varchar)   || '-' ||
            local.sentido               || '-' ||
            local.uf_sigla              || '-' ||
            local.municipio             || '-' ||
            local.tipo_area             || '-' ||

            categoria.tipo_acidente     || '-' ||
            categoria.causa_acidente    || '-' ||
            categoria.classificacao_acidente
        ) as id,

        local.br, 
        local.km, 
        local.sentido,
        local.uf_sigla, 
        local.municipio,
        local.tipo_area, 

        categoria.tipo_acidente,
        categoria.causa_acidente,
        categoria.classificacao_acidente,

        cast(sum(fato.total_mortos) as bigint) as total_mortos,
        cast(sum(fato.total_pessoas_envolvidas) as bigint) as total_envolvidos,
        cast(count(fato.id) as bigint) as total_ocorrencias,

        round(
            cast(sum(fato.total_mortos) as decimal(5, 2)) 
            / nullif(cast(sum(fato.total_pessoas_envolvidas) as decimal(5, 2)), 0), 2
        ) as taxa_mortalidade_envolvido,
        round(
            cast(sum(fato.total_mortos) as decimal(5, 2)) 
            / nullif(cast(count(fato.id) as decimal(5, 2)), 0), 2
        ) as taxa_mortalidade_ocorrencia

    from {{ ref('fct_ocorrencia') }} fato

    join {{ ref('dim_local') }}  local
        on fato.sk_local = local.sk_local

    join {{ ref('dim_categoria') }} categoria
        on fato.sk_categoria = categoria.sk_categoria

    group by
        local.br, 
        local.km, 
        local.sentido,
        local.uf_sigla, 
        local.municipio,
        local.tipo_area,

        categoria.tipo_acidente,
        categoria.causa_acidente,
        categoria.classificacao_acidente
)

select * from aggregation

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} 
        where {{ this }}.id = aggregation.id
    )
{% endif %}