{{
    config(
        materialized='incremental',
        unique_key='id',    
    )
}}

with 

local as (
    select
        sk_local,
        br, 
        km, 
        sentido,
        uf_sigla, 
        uf_nome, 
        municipio,
        tipo_area
    from {{ ref('dim_local') }}
),

categoria as (
    select * from {{ ref('dim_categoria') }}
),

aggregation as (
    select
        local.sk_local,
        categoria.sk_categoria,

        cast(count(fato.id) as bigint) as total_ocorrencias,
        cast(sum(fato.total_mortos) as bigint) as total_mortos,
        cast(sum(fato.total_envolvidos) as bigint) as total_envolvidos,

        cast(
            round(sum(fato.total_mortos)/ nullif(sum(fato.total_envolvidos), 0), 2) 
            as decimal(5, 2)
        ) as taxa_mortalidade,
        cast(
            round(sum(fato.total_mortos) / nullif(count(fato.id), 0), 2)
            as decimal(5, 2)
        ) as media_mortalidade

    from {{ ref('fct_ocorrencia') }} fato
    join local on fato.sk_local = local.sk_local
    join categoria on fato.sk_categoria = categoria.sk_categoria

    group by
        local.sk_local,
        categoria.sk_categoria
),
description as (
    select 
        md5(aggregation.sk_local || '-' || aggregation.sk_categoria) as id,

        local.br,
        local.km,
        local.sentido,
        local.uf_sigla,
        local.uf_nome,
        local.municipio,
        local.tipo_area,
        categoria.tipo_acidente,
        categoria.causa_acidente,
        categoria.classificacao_acidente,

        total_mortos,
        total_envolvidos,
        total_ocorrencias,
        taxa_mortalidade,
        media_mortalidade
        
    from aggregation
    join local on aggregation.sk_local = local.sk_local
    join categoria on aggregation.sk_categoria = categoria.sk_categoria
)

select * from description

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} 
        where {{ this }}.id = description.id
    )
{% endif %}