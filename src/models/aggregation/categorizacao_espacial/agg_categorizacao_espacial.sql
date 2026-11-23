{{
    config(
        materialized='incremental',
        unique_key='id',    
    )
}}

with 

staging as (
    select distinct
        sk_malha_geografica,
        sk_malha_rodoviaria,
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
        sk_malha_geografica,
        sk_malha_rodoviaria,
        sk_categoria
),

aggregation as (
    select
        md5(
            staging.sk_malha_geografica || '-' || 
            staging.sk_malha_rodoviaria || '-' || 
            staging.sk_categoria
        ) as id,

        malha_geografica.regiao,
        malha_geografica.estado,
        malha_geografica.tipo_area,
        malha_rodoviaria.br,

        categoria.tipo_acidente,
        categoria.causa_acidente,
        categoria.classificacao_acidente,
        
        staging.total_ocorrencias,
        staging.taxa_mortalidade,
        staging.indice_mortalidade_ocorrencia,
        staging.indice_envolvimento_ocorrencia
    from staging

    inner join {{ ref('dim_malha_geografica') }} as malha_geografica
        on staging.sk_malha_geografica = malha_geografica.sk_malha_geografica

    inner join {{ ref('dim_malha_rodoviaria') }} as malha_rodoviaria
        on staging.sk_malha_rodoviaria = malha_rodoviaria.sk_malha_rodoviaria

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