{{
    config(
        materialized='incremental',
        unique_key='id',    
    )
}}

with 

staging as (
    select distinct
        sk_tempo,
        sk_clima,
        sk_malha_geografica,
        sk_categoria,

        cast(count(id) as bigint) as total_ocorrencias,

        cast(
            round(sum(total_mortos)::decimal / nullif(sum(total_envolvidos), 0), 2) 
            as decimal(5, 2)
        ) as taxa_mortalidade,
        cast(
            round(sum(total_mortos)::decimal / nullif(count(id), 0), 2)
            as decimal(5, 2)
        ) as indice_mortalidade_ocorrencia

    from {{ ref('fct_ocorrencia') }}

    group by
        sk_tempo,
        sk_clima,
        sk_malha_geografica,
        sk_categoria
),

aggregation as (
    select
        md5(
            staging.sk_tempo            || '-' || 
            staging.sk_clima            || '-' || 
            staging.sk_malha_geografica || '-' ||
            staging.sk_categoria
        ) as id, 

        tempo.mes,
        tempo.mes_nome,
        malha_geografica.regiao,
        malha_geografica.estado,
        clima.condicao_metereologica as condicao_climatica,

        staging.total_ocorrencias,
        staging.taxa_mortalidade,
        staging.indice_mortalidade_ocorrencia

    from staging

    join {{ ref('dim_tempo') }} as tempo
        on staging.sk_tempo = tempo.sk_tempo

    join {{ ref('dim_clima') }} as clima
        on staging.sk_clima = clima.sk_clima

    join {{ ref('dim_malha_geografica') }} as malha_geografica
        on staging.sk_malha_geografica = malha_geografica.sk_malha_geografica

    join {{ ref('dim_categoria') }} as categoria
        on staging.sk_categoria = categoria.sk_categoria

    where categoria.classificacao_acidente = 'com vítimas fatais'
        or categoria.classificacao_acidente = 'com vítimas feridas'
),

select * from aggregation

{% if is_incremental() %}
where not exists (
    select 1 from {{ this }} as this
    where this.id = aggregation.id
)
{% endif %}